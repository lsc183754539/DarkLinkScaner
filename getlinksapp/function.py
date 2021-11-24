import bs4
import re
import requests
import time
from datetime import datetime
from getlinksapp.models import linksData


def getResCode(url):
    try:
        response = requests.get(url, verify=False, timeout=3)
        return response.status_code
    except:
        return 0


# 引入定义敏感词
with open('./getlinksapp/rules.txt', 'r', encoding='utf-8') as rd:
    minganci_list = rd.read()


# 检查内容违规
def checkMinganci(response_text):
    abnormalPoint = re.findall(minganci_list, response_text)
    print(abnormalPoint)
    if len(abnormalPoint) != 0:
        abnormal = True
    else:
        abnormal = False
    return abnormal, abnormalPoint


def saveData(domain, link, fromUrl, resCode, abnormal, abnormalPoint):
    link_object = linksData()
    link_object.mission = domain
    link_object.link = link
    link_object.response_code = resCode
    link_object.from_link = fromUrl
    link_object.abnormal = abnormal
    link_object.abnormal_point = abnormalPoint
    link_object.find_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    link_object.save()


# 1.正则匹配文章中的链接并做检查
def getLinks_by_re(res):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    find_url_temp = re.findall(pattern, res.text.replace(' ', ''))

    # 正则匹配还是有问题，清除连接中的特殊符号如逗号分号
    find_url = []
    for item in find_url_temp:
        item = re.sub(r"<.*>", "", item)  # 去掉标签内容
        item = item.replace("'", '').replace(";", "")
        item = re.sub(r"<.*", "", item)
        find_url.append(item)

    return find_url
    pass


def getLinks(url, domain):
    print(url)

    # 获取当前链接域名信息，为后面不带有域名信息的链接构建域名（传过来的url必定带http://域名信息）
    url_domain = url
    url_list = url_domain.split('/')
    if len(url_list) > 3:
        url_domain = 'http://' + ''.join(url_list[2])
        # print(url_domain)  # 获得域名信息

    # 请求网页内容

    headers = {"User-Agent": "CERNET URL SAFE SCAN SYSTEM. JUST FOR SHANDONG EDU DOMAIN."}
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=3)  # 去掉SSL证书检查
    except:
        # 调用腾讯云函数异地检测，返回异地检测结果
        # return tencent_cloud_function(url) # 还没写，也没部署

        print('[x]请求出错！仔细阅读使用说明！')
        print('[x]请求出错！仔细阅读使用说明！')
        print('[x]请求出错！仔细阅读使用说明！')
        pass

    # 1.正则匹配文章中的链接并做检查
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    find_url_temp = re.findall(pattern, res.text.replace(' ', ''))

    # 正则匹配还是有问题，清除连接中的特殊符号如逗号分号
    find_url = []
    for item in find_url_temp:
        item = re.sub(r"<.*>", "", item)  # 去掉标签内容
        item = item.replace("'", '').replace(";", "")
        item = re.sub(r"<.*", "", item)
        find_url.append(item)

    for link in find_url:  # find_url 是个列表，可能为空，则直接跳过该段代码
        if linksData.objects.filter(link__exact=link):
            continue
        else:
            rescode = getResCode(link)  # 获取状态值
            try:
                r = requests.get(link, headers=headers, verify=False)
                r.encoding = r.apparent_encoding if r.encoding == 'ISO-8859-1' else r.encoding
            except:
                continue
            try:
                abnormal, abnormalPoint = checkMinganci(r.text)  # 检测敏感词
                saveData(domain, link, url, rescode, abnormal, abnormalPoint)  # 保存数据
            except:
                saveData(domain, link, url, rescode, False, [])  # 保存数据
        if str(domain) in link:
            getLinks(link, domain=domain)  # 域内未收录链接创建任务继续迭代

    # 2.排查<a>标签中的链接并作检查
    soup = bs4.BeautifulSoup(res.text, "lxml")
    for links in soup.findAll('a', attrs={'href': re.compile("/")}):
        # 筛选<a>标签中带有http/https的链接信息（第一种）
        link = links.get('href')
        if 'http://' in link or 'https://' in link:
            if linksData.objects.filter(link__exact=link):
                continue
            else:
                rescode = getResCode(link)  # 获取状态值
                try:
                    r = requests.get(link, headers=headers, verify=False)
                    r.encoding = r.apparent_encoding if r.encoding == 'ISO-8859-1' else r.encoding
                except:
                    continue
                try:
                    abnormal, abnormalPoint = checkMinganci(r.text)  # 检测敏感词
                    saveData(domain, link, url, rescode, abnormal, abnormalPoint)  # 保存数据
                except:
                    saveData(domain, link, url, rescode, False, [])  # 保存数据

            # 若获取到的链接是域内链接，则作为母链接继续向下发现链接
            if str(domain) in str(link):
                getLinks(link, domain=domain)

        # 筛选<a>标签中不带有域名信息的链接
        else:
            if link[0] != '/':
                if '../' in link:
                    link = link.replace('../', '')
                link = url_domain + '/' + link
            else:
                link = url_domain + link

            if linksData.objects.filter(link__exact=link):
                continue
            else:
                rescode = getResCode(link)  # 获取状态值
                try:
                    r = requests.get(link, headers=headers, verify=False)
                    r.encoding = r.apparent_encoding if r.encoding == 'ISO-8859-1' else r.encoding
                except:
                    continue
                try:
                    abnormal, abnormalPoint = checkMinganci(r.text)  # 检测敏感词
                    saveData(domain, link, url, rescode, abnormal, abnormalPoint)  # 保存数据
                except:
                    saveData(domain, link, url, rescode, False, [])  # 保存数据

            # 域内链接，作为母链接继续向下发现链接
            if str(domain) in link:
                getLinks(link, domain=domain)

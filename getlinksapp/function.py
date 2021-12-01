import bs4
import re
import requests
from datetime import datetime
from getlinksapp.models import linksData

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


# 忽略https有效性验证警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 获取请求内容，单独择出来，减少代码量，控制请求次数。
def getRes(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
        response = requests.get(url, headers=headers, allow_redirects=True, verify=False)
        return response.status_code, response
    except:
        return 0, None


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


# 打算重写代码，再说再说
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
    print('RE FIND URL:', find_url)
    return find_url


# 2.排查<a>标签中的链接并作检查
def getLinks_by_soup(res, url):
    find_url_temp = []
    find_url = []
    url_domain = url
    url_list = url_domain.split('/')
    if len(url_list) > 3:
        url_domain = 'http://' + ''.join(url_list[2])
    soup = bs4.BeautifulSoup(res.text, "lxml")
    try:
        if_location = re.findall(r'[\'](.*?)[\']', str(soup))
        for item in if_location:
            find_url_temp.append(item)
    except:
        pass
    find_url_lxml_list = soup.findAll('a', attrs={'href': re.compile("/")})
    for links in find_url_lxml_list:
        find_url_temp.append(links.get('href'))
    for link in find_url_temp:
        if url_domain in link or 'http://' in link or 'https://' in link:
            find_url.append(link)
        else:
            if link[0] != '/':
                if '../' in link:
                    link = link.replace('../', '')
                link = url_domain + '/' + link
                find_url.append(link)
            else:
                link = url_domain + link
                find_url.append(link)
    print('SOUP FIND URL:', find_url)
    return find_url


def HandleandSave(find_url, domain, url):
    for link in find_url:  # find_url 是个列表，可能为空，则直接跳过该段代码
        if linksData.objects.filter(link__exact=link):
            continue
        else:
            res_code, res_content_2 = getRes(link)  # 获取状态值
            try:
                res_content_2.encoding = res_content_2.apparent_encoding if res_content_2.encoding == 'ISO-8859-1' else res_content_2.encoding
            except:
                continue
            try:
                abnormal, abnormalPoint = checkMinganci(res_content_2.text)  # 检测敏感词
                saveData(domain, link, url, res_code, abnormal, abnormalPoint)  # 保存数据
            except:
                saveData(domain, link, url, res_code, False, [])  # 保存数据
        if str(domain) in link:
            getLinks(link, domain=domain)  # 域内未收录链接创建任务继续迭代
            print(link, '下探扫描完成！')
            # 筛选<a>标签中不带有域名信息的链接


def getLinks(url, domain):
    # 获取链接的内容
    print(url)
    res_code, res_content = getRes(url)

    # 1.正则匹配文章中的链接并做检查
    find_url = getLinks_by_re(res_content)
    HandleandSave(find_url, domain, url)

    # 2.排查<a>标签中的链接并作检查
    find_url = getLinks_by_soup(res_content, url)
    HandleandSave(find_url, domain, url)

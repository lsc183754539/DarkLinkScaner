# DarkLink

#### 介绍
{**DarkLink**
针对域的暗链接扫描系统，可以对网站进行多级页面的抓取分析，发现失效链接及敏感内容链接。}
![系统截图](https://images.gitee.com/uploads/images/2021/1117/111941_a326bd9d_1668500.png "微信图片_20211117111926.png")

#### 软件架构

基于Python3 及 Django3框架 开发的网站暗链接检测系统。


#### 安装教程

1.  `git clone https://gitee.com/pasalai/DarkLink.git `
2.  `cd DarkLink`
3.  `python -m pip install -r requirements.txt`
4.  `python manage.py runserver 0.0.0.0:8000`
5.  使用浏览器访问http://127.0.0.1:8000 , 用户名为`admin`，密码为`password`  

#### 使用说明

1.  扫描针对的是**域**，请先在域列表中添加域信息，如：`sdu.edu.cn`(==\*.sdu.edu.cn + sdu.edu.cn)或`jwc.sdu.edu.cn` (==\*.jwc.sdu.edu.cn + jwc.sdu.edu.cn)
2.  任务列表中的链接地址仅作为抓取的起点链接，建议填写主页，对未出现的信息孤岛链接建议另行添加域及任务
3.  目前系统并非多线程，若想同时扫描多个任务，请修改`getlinksapp/views.py` 的`start_scan()`函数
4.  若运行过程中提示`远程主机断开连接`等错误导致程序终止，请更换网络环境
5.  若使用过程中出现任何问题或疑惑，请提交Issues

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_DarkLink 分支
3.  提交代码
4.  新建 Pull Request

#### 贡献者

1.  Nobady yet
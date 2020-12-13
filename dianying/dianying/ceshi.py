# 此文件为我编写代码过程中，某一个步骤测试文件，单独来测试功能
import requests
from lxml import etree
import time
# a = 1
# url = 'http://www.xidianying.com/list-56-{}.html'
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3776.400 QQBrowser',
# }
# start_urls = url.format(a)
# html = requests.get(start_urls,headers=headers).text
#
# # 这里将str格式的html转换为xpath能解析的对象
# html = etree.HTML(html)
#
#
#
#
# # url = 'http://www.xidianying.com/dianying/145060.html'
# def get_url(url):
#     html = requests.get(url).text
#     html = etree.HTML(html)
#     baiduurl = ''
#     tiquma = ''
#     # 因为有的页面有多个a标签所以我们要排除这种可能,
#     lists = html.xpath("//td[@class='t_f']//a/@href")
#     for list in lists:
#         if 'baidu.com' in list:
#             baiduurl= str(list)
#     all= html.xpath("//td[@class='t_f']//text()")
#     for i in all:
#         a = '提取'
#         if a in i:
#             tiquma = i
#     return baiduurl,tiquma
#
#
# # 接卸出tbody标签ID以normalthread开头的元素
# lists = html.xpath("//tbody[starts-with(@id,'normalthread')]")
# for list in lists:
#     b = '百度云'
#     # 获取所有的标题和网址
#     name = list.xpath("./tr/th/a[2]/text()")
#     print(name)
#     name = ''.join(name)
#     # 筛选出百度云的链接
#     if b in name:
#         url = list.xpath("./tr/th/a[2]/@href")
#         url = ''.join(url)
#         baiduurl,tiquma = get_url(url)
#
#         print(name,baiduurl,tiquma)
#
#     time.sleep(2)
#
#
#
# # a = get_url(url)
# # print(a)

#  测试代理能不能正常获取

url = 'http://127.0.0.1:5000/random'
response = requests.get(url)
print(response.text)
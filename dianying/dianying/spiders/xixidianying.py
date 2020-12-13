import scrapy
import requests
from lxml import etree
from dianying.items import DianyingItem
from scrapy_redis.spiders import RedisSpider


class XixidianyingSpider(scrapy.Spider):
    name = 'xixidianying'
    allowed_domains = ['xidianying.com']
    url = 'http://www.xidianying.com/list-56-{}.html'
    # urls = url.format(str(offset))
    # start_urls = ['xixidianying']
    # redis_key = 'xixidianying'

    def get_url(self,url):
        # 获取网页的源代码
        html = requests.get(url).text
        # 将网页源码转换为可xpath解析的对象
        html = etree.HTML(html)
        baiduurl = ''
        tiquma = ''
        # 经过分析，我们发现个别页面有多个a标签所以我们要排除这种可能,只选出云盘的链接
        # 先筛选出所有的A标签
        lists = html.xpath("//td[@class='t_f']//a/@href")
        # 经过测试，不管只有一个a标签，还是返回多个，它都是列表的形式返回的，所以我们直接循环
        for list in lists:
            if 'baidu.com' in list:
                # 这块转换str是因为如果是多个a标签的话，list是lxml的unicode对象,所以先进行转换
                baiduurl = str(list)
        all = html.xpath("//td[@class='t_f']//text()")
        for i in all:
            a = '提取'
            if a in i:
                tiquma = i
        return baiduurl,tiquma

    def start_requests(self):
        for i in range(1,11):
            yield scrapy.Request(self.url.format(str(i)),callback=self.parse_get)

    def parse_get(self,response):
        print('开始爬取')
        item = DianyingItem()
        lists = response.xpath("//tbody[starts-with(@id,'normalthread')]")
        for list in lists:
            b = '百度云'
            # 获取所有的标题和网址
            print('获取标题')
            lname = list.xpath("./tr/th/a[2]/text()").extract()

            # 返回的是list，我们转化为str
            names = ''.join(lname)
            print(names)
            # 筛选出百度云的链接
            if b in names:
                print('资源网址：')
                lurl = list.xpath("./tr/th/a[2]/@href").extract()

                # 同上进行str转换
                urls = ''.join(lurl)
                print(urls)
                baiduurl, tiquma = self.get_url(urls)
                print(baiduurl, tiquma)
                item['name'] = names
                item['baiduurl'] = baiduurl
                item['tiquma'] = tiquma

                yield item
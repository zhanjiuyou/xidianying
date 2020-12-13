import scrapy
from dianying.items import DianyingItem

class XixiSpider(scrapy.Spider):
    name = 'xixi'
    allowed_domains = ['www.xidianying.com']
    # start_urls = ['http://www.xidianying.com/']
    # 这块构建url链接
    url = 'http://www.xidianying.com/list-56-{}.html'
    # 重构start-request函数，scrapy调用时是从这里读取链接
    def start_requests(self):
        for i in range(1,11):
            yield scrapy.Request(self.url.format(str(i)),callback=self.parse)

    def parse(self, response):
        print('开始爬取')
        # 分析网页，找出所有的链接
        lists = response.xpath("//tbody[starts-with(@id,'normalthread')]")
        for list in lists:
            b = '百度云'
            # 获取所有的标题和网址
            print('获取标题')
            lname = list.xpath("./tr/th/a[2]/text()").extract()
            # 返回的结果是list，我们转化为str格式
            names = ''.join(lname)
            print('标题为:',names)
            # 筛选出百度云关键字的链接，如果标题中含有百度云三个字，则提取herf
            if b in names:
                lurl = list.xpath("./tr/th/a[2]/@href").extract()
                # 同上进行结果是list，转换为str格式
                urls = ''.join(lurl)
                print("资源网址为：",urls)
                yield scrapy.Request(urls,callback=self.parse_onepage)

    # 这个函数为资源页面的百度云链接和提取码的分析
    def parse_onepage(self,response):
        item = DianyingItem()
        # 获取目标网页中的href，有可能包含多个href，且返回结果为list了，所以我们进行遍历
        print('获取页面中的所有链接')
        lists = response.xpath("//td[@class='t_f']//a/@href").extract()
        for list in lists:
            if 'baidu.com' in list:
                # 这块转换str是因为如果是多个a标签的话，list是lxml的unicode对象,所以先进行转换
                item['baiduurl'] = str(list)

        # 获取页面中的所有文本，找到提取码
        all = response.xpath("//td[@class='t_f']//text()").extract()
        for i in all:
            a = '提取'
            if a in i:
                item['tiquma'] = i

        # 获取该链接的标题
        name = response.xpath("//span[@id='thread_subject']/text()").extract_first()
        item['name'] = name
        yield item



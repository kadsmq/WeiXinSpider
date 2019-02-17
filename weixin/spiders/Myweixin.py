# -*- coding: utf-8 -*-
import scrapy
from weixin.items import WeixinItem

class MyweixinSpider(scrapy.Spider):
    name = 'Myweixin'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    start_urls = ['https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%B5%81%E6%B5%AA%E5%9C%B0%E7%90%83&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2040&sst0=1550402042964&lkt=1%2C1550402042862%2C1550402042862']

    def parse(self, response):
        item = WeixinItem()

        li_list = response.xpath('//*[@id="main"]/div[5]/ul/li')
        for li in li_list:
            item['article_urlx'] = li.xpath('./div[2]/h3/a/@href').extract_first()
            item['writer'] = li.xpath('./div[2]/div/a/text()').extract_first()
            item['intro'] = li.xpath('./div[2]/div/span/text()[1]').extract_first()
            # 名字根据颜色不同在xpath里应该得拆分成3个
            name_q = li.xpath('./div[2]/h3/a/text()[1]').extract_first()
            name_red = li.xpath('./div[2]/h3/a/em/text()[1]').extract_first()
            name_h = li.xpath('./div[2]/h3/a/text()[2]').extract_first()
            item['article_title'] = str(name_q) + str(name_red) + str(name_h)
            yield scrapy.Request(item['article_urlx'], callback=self.parse_ziye,meta=item)
        
        # 构造翻页，url需要拼接
        url_0 = 'https://weixin.sogou.com/weixin'
        url_1 = response.xpath('//*[@id="sogou_next"]/@href').extract_first()
        if url_1 is not None:
            url_max = url_0 + url_1
            yield scrapy.Request(url_max, callback=self.parse)
        else:
            print('******木有下一页了******')
            
    def parse_ziye(self, response):
        item = response.meta
        item['article_urly'] = response.xpath('//*[@id="js_sg_bar"]/a/@href').extract_first()
        yield item

# -*- coding: utf-8 -*-
import scrapy
from ..items import ErshoufangItem
from datetime import datetime, timedelta
from twisted.internet.error import TimeoutError
import math
import time
import re
import requests
from bs4 import BeautifulSoup

class ErshoufangSpider(scrapy.Spider):

    name = 'ershoufang'
    allowed_domains = ['bj.5i5j.com']
    #start_urls = ['https://hz.5i5j.com/ershoufang/o8/']
    base_url = 'https://bj.5i5j.com/zufang/n354'
    #1-33 34-51 52-77 78-103 104-123 124-147 148-189
    #241  354
    l = []

    #['124.238.157.115', '124.238.157.115', '202.112.237.102', '124.238.157.115', '5.8.207.160', '124.238.157.115', '124.238.157.115', '165.227.30.201', '124.238.157.115', '223.85.196.75', '110.52.235.84', '103.22.173.230', '51.83.47.73', '190.109.169.41', '124.238.157.115', '13.127.2.151', '190.147.207.101', '13.127.2.151', '70.65.233.174', '183.203.96.125', '27.191.234.69', '61.19.145.66', '194.76.138.111', '124.238.157.115', '124.238.157.115', '111.40.84.73', '124.238.157.115', '122.146.68.17', '124.238.157.115', '120.131.7.227', '14.249.166.4']
    #根据房源数计算页数
    num = math.ceil(29875/30)

    custom_settings = {
        #以运行爬虫的日期命名csv文件
        'FEED_URI' : './{}.csv'.format(datetime.now().strftime('%Y%m%d')),
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING' : 'utf8'
    }


    def start_requests(self):
        # 分若干段下载，根据代理池可用代理数量来考虑
        #offset = 500
        # for n in range(0, self.num, offset):
        #     yield scrapy.Request(self.base_url.format(n+1), meta={'start':n, 'offset':offset}, dont_filter=True)
        # for n in range(0, 5):
        #     #self.num
        #     yield scrapy.Request(self.base_url.format(n+1), meta={'start':n}, dont_filter=True)
        yield scrapy.Request(self.base_url, meta={'cookiejar':1}, callback=self.parse, dont_filter=True)


    def parse(self, response):
        #print(response.)
        status = response.status
        print('响应状态码 = %d'%status )
        s_l = [401,402,403]
        if status in s_l:
            print('捕捉到%d'%status )
            print(response.text)
            yield scrapy.Request(self.base_url, meta={'cookiejar': 1}, callback=self.parse, dont_filter=True)
        else:
            #window.location.href='https://bj.5i5j.com/zufang/n2/?y=c7f1d18e83cd173c_1556118546';
            html =response.text
            title = response.css("title::text").extract_first()
            #print(html)
            re1 = r'<script>window.location.href=(.*?);</script>'
            #re_url = re.compile(re1)
            red_url = re.findall(re1, html, re.S)
            print(red_url)

            if title == '403 Forbidden':
                s_url = response.css(".page-bottom-word p span::text")[1].extract()
                s_ip = response.css(".page-bottom-word p span::text")[3].extract()
                print("这个IP被封了" + s_ip)
                self.l.append(s_ip)
                print(self.l)
                yield scrapy.Request(s_url, meta={'cookiejar':True}, callback=self.parse, dont_filter=True)
            else:
                if len(red_url)>0 :
                    redr_url = red_url[0].replace('\'','')
                    print(redr_url)
                    yield scrapy.Request(redr_url, meta={'cookiejar':1}, callback=self.parse, dont_filter=True, errback=self.errback_parse)
                else:
                    divs= response.css('div.listCon')

                    # 响应Cookies
                    Cookie1 = response.headers.getlist('Set-Cookie')  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
                    print('后台首次写入的响应Cookies：', Cookie1)

                    for d in divs:
                        item = ErshoufangItem()
                        item['title'] = d.css('h3 a::text').extract_first()
                        item['href'] = d.css('h3 a::attr(href)').extract_first()
                        item['tags'] = d.css('.listTag span::text').extract()   #标签
                        item['price'] = d.css('.jia p.redC strong::text').extract_first() + d.css('.jia p.redC::text').extract_first().strip().replace(' ','')
                        try:
                            item['h_method'] = d.css('.jia p::text')[1].extract().split('：')[1]   #出租方式
                        except:
                            item['h_method'] = ''
                        infos = d.css('.listX p::text')[0].extract().split('·')
                        item['huxing'] = infos[0].replace(' ','')   #户型
                        item['square'] = infos[1].replace(' ','')   #面积
                        item['orientation'] = infos[2].strip()   #朝向
                        item['floor'] = infos[3].strip()   #楼层
                        try:
                            item['renovation'] = infos[4].strip()   #装修(可能没有)
                        except:
                            item['renovation'] = ''
                        item['area'] = d.css('.listX p a::text').extract_first()  #区域,小区
                        #d.css('.listX p a::text').extract()
                        try:
                            item['metro'] = d.css('.listX p::text')[1].extract().split('·')[1].strip()   #地铁(可能没有)
                        except:
                            item['metro'] = ''

                        infos1 = d.css('.listX p::text')[2].extract().split('·')
                        try:
                            item['view'] = infos1[1].strip()
                        except:
                            item['view'] = ''
                        try:
                            t = infos1[2].replace('发布','')
                            t = t.replace(' ','')
                            if t == '今天':
                                t = datetime.now()
                            elif t == '昨天':
                                t = datetime.now() - timedelta(days=1)
                            else:
                                t = datetime.strptime(t, '%Y-%m-%d')
                            #日期转换为字符串格式
                            item['time'] = t.strftime('%Y-%m-%d')
                        except:
                            item['time'] = ''
                        yield item


                        #分页
                    next_p = response.css("a.cPage::attr(href)").extract_first()
                    #/html/body/div[4]/div[1]/div[3]/div[2]/a[1]
                    cur_p = response.css('.pageBox div.pageSty.rf a.cur::text').extract_first()
                    try:
                        print('尝试提取下一个页面!!!!' + next_p)
                    except:
                        print(response.text)
                        time.sleep(1)

                    #start = response.meta['start']
                    #offset = response.meta['offset']

                    if next_p is not None:
                    # if next_p is not None and int(cur_p) < (start + offset):
                    #if len(next_p) is not None:
                        #yield response.follow(next_p, callback=self.parse, meta={'start':start, 'offset':offset}, errback=self.errback_parse)
                        # time.sleep(1)
                        yield response.follow(next_p, meta={'cookiejar':True}, callback=self.parse,errback=self.errback_parse)
                        self.logger.info('当前页<{}>已完成提取，有下一页:{}'.format(cur_p, next_p))

                    else:
                        self.logger.info('最后一页<{}>已完成提取'.format(cur_p))



    #html.headers['Location']

    def get_proxy(self, i):
        if i > 3:
            r = requests.get('http://127.0.0.1:5555/random')
            proxy = BeautifulSoup(r.text, "lxml").get_text()
            return proxy
        else:
            return None

    #
    def errback_parse(self, failure):
        self.logger.error(repr(failure))

        if failure.check(TimeoutError):
            url = failure.request.url
            #不能加errback参数，否则无限循环
            self.logger.debug('超时，失败次数过多，重新发起一次该请求 {}'.format(url))
            print('超时，失败次数过多，重新发起一次该请求 {}'.format(url))
            yield scrapy.Request(url, meta={'cookiejar':1}, callback=self.parse, dont_filter=True)

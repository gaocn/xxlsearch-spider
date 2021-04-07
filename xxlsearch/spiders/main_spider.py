import scrapy
import numpy
from scrapy.mail import MailSender
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from xxlsearch.items import XxlsearchItem


class MainSpider(scrapy.Spider):
    """
        查找‘放射性废物处置’相关项目招标书
    """
    name = "xxlsearch"
    search_key_words = [
        "放射性废物处置",
        "放废处置",
        "放废处理",
        "三废治理",
        "放废管理",
        "极低放",
        "填埋场",
        "低放平放射性",
        "低水平放射性",
        "中放平放射性",
        "中水平放射性",
        "中等深度放射性",
        "高放放射性",
        "高水平放射性",
        "乏燃料",
        "玻璃固化",
        "地下实验室",
        "退役",
        "容器",
        "处置容器",
        "贮存",
        "贮存库",
        "西北",
        "龙和",
        "飞凤山",
        "北山",
        "安全评价",
        "安分",
        "环评",
        "安全全过程系统分析",
        "深地质",
        "缓冲材料",
        "回填材料",
        "地下实验室",
        "阳江",
        "岩洞处置",
        "核素迁移",
        "废源",
        "废密封源",
        "废放射源",
        "福建核电环保配套",
        "浙江核电环保配套",
        "徐大堡核电环保配套",
        "防城港核电环保配套",
        "废矿井",
        "神仙洞",
        "NORM",
        "伴生",
        "深钻孔",
        "粘土岩",
        "花岗岩",
        "处置概念",
        "工程屏障",
        "地球化学屏障",
        "混凝土",
        "处置工艺",
        "源项调查",
        "景象FEPS",
        "监测",
        "风蚀",
        "覆盖层",
        "核设施拆除",
        "整备",
        "废矿井",
        "处置机具装备",
        "处置工程设计",
        "气候长期演化",
        "选址准则",
        "选址",
        "放射性废物处置",
        "放射性废物",
        "废物处置",
        "处置",
        "废物",
        "放射性"
    ]
    search_urls = [
        'https://www.dlzb.com/zb/',
        'https://www.chinabidding.cn/17728_cw/',
        'http://www.sastind.gov.cn/n157/index.html',
        'http://www.mod.gov.cn/topnews/node_47615.htm'
    ]

    link_extractor = LxmlLinkExtractor()

    mailer = MailSender(
        smtphost='smtp.163.com',
        smtpport=25,
        smtpuser='gaowenwencn@163.com',
        mailfrom='gaowenwencn@163.com',
        smtppass='ISIQFLTYGQZLCZTU'
    )

    def start_requests(self):
        for url in self.search_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for url_text in response.xpath('//a/text()'):
        #     self.log(url_text.get())

        # 中核集团电子采购平台
        # [contains(@class, "keyth_title")]
        # for element in response.xpath('//a'):
        #     url = element.get()
        #     for key_words in self.search_key_words:
        #         if key_words in url:
        #             self.log(url)

        #  [not(contains(@class, "keyth_title"))]
        # for element in response.xpath('//a'):
        #     url_text = element.xpath('string(.)').extract()[0]
        #     if url_text.isnumeric() and int(url_text) < 50:
        #         next_page = element.xpath('@href').get()
        #         if next_page is not None:
        #             # self.log("翻页" + next_page)
        #             yield scrapy.Request(next_page, callback=self.parse)
        wanted_links = []
        for link in self.link_extractor.extract_links(response):
            for key_words in self.search_key_words:
                if key_words in link.text:
                    if '招标公告' in link.text:
                        wanted_links.append(link)
            yield scrapy.Request(link.url, callback=self.parse)

        if len(wanted_links) > 0:
            content = ''
            for l in wanted_links:
                content += f"""
                        标题：{l.text}  链接：{l.url}
                
                """
            body = f"""
                    小主，

                       下面是我爬取到的结果，希望对你有所帮助，你可以点击链接确认一下结果。O(∩_∩)O哈哈~
                            
                    =========================================================================        
                       {content}
                    =========================================================================     
                    来自网络爬虫
                    """
            # body = MIMEText(body, _subtype='html', _charset='utf8')
            self.mailer.send(
                to=["wudanqingcn@163.com", "wdq@cnpe.cc"],
                subject="【来自爬虫】爬取结果",
                body=body
            )

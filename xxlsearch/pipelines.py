# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from logging import Logger
from logging import DEBUG
from email.mime.text import MIMEText
from scrapy.mail import MailSender


class XxlsearchPipeline:
    logger = Logger(__name__)

    def __init__(self):
        self.mailer = MailSender(
            smtphost='smtp.163.com',
            smtpport=25,
            smtpuser='gaowenwencn@163.com',
            mailfrom='gaowenwencn@163.com',
            smtppass='ISIQFLTYGQZLCZTU'
        )

    def send_email(self, content):
        self.mailer.send(
            to=["wudanqingcn@163.com"],
            subject="【爬虫】今天查找结果",
            body=content
        )
        self.logger.log(DEBUG, '发送成功')

    def process_item(self, item, spider):
        content = f"""
        主人好，
            下面是我爬取到的结果，希望对你有所帮助，你可以点击链接确认一下结果。O(∩_∩)O哈哈~
            <br/>
            <style type="text/css">
                table.gridtable {{
                    font-family: verdana,arial,sans-serif;
                    font-size:11px;
                    color:#333333;
                    border-width: 1px;
                    border-color: #666666;
                    border-collapse: collapse;
                }}
                table.gridtable th {{
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #dedede;
                }}
                table.gridtable td {{
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #ffffff;
                }}
                </style>
                 
                <table class="gridtable">
                <tr>
                    <th>标题</th><th>链接</th>
                </tr>
                <tr>
                    <td>{item.title}</td><td><a href='{item.url}'>{item.url}</a></td>
                </tr>
                </table>
        """
        body = MIMEText(content, _subtype='html', _charset='utf8')
        self.send_email(body.as_string())

        self.logger.log(DEBUG, body.as_string())
        self.logger.log(DEBUG, f"item found: {item.title}")

        return item

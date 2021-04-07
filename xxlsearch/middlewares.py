# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import IgnoreRequest
from pybloom_live import ScalableBloomFilter
import hashlib


class IgnoreRequestMiddleware(object):
    """
        url 请求去重
    """
    def __init__(self):
        # 可自动伸缩的布隆过滤器
        self.sbf = ScalableBloomFilter(initial_capacity=100,error_rate=0.001)

    def process_request(self, request, spider):
        if not request.url:
            return None
        url_hash = hashlib.md5(request.url.encode("utf8")).hexdigest()
        if url_hash in self.sbf:
            raise IgnoreRequest("Spider : %s, IgnoreRequest : %s" % (spider.name, request.url))
        else:
            self.sbf.add(url_hash)

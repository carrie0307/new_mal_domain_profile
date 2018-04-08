# encoding:utf-8

"""
IP历史状态探测handler
"""
import tornado.web
import json
from base_handler import BaseHandler
from models.get_ip_history import IP_history

default_domain = '000033333.com'
class IPHistoryHandler(BaseHandler):
    """IP历史状态探测控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        self.render(
            'ip_history.html',
            domain = json.dumps(domain),
        )

class IPHistoryDataHandler(BaseHandler):
    """IP历史页面控制"""
    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        res = IP_history(domain).get_history_record()
        self.write(json.dumps(res))

class WhoisHistoryHandler(BaseHandler):
    """IP历史状态探测控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        self.render(
            'whois_history.html',
            domain = json.dumps(domain),
        )

class ContentHistoryHandler(BaseHandler):
    """IP历史状态探测控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        self.render(
            'content_history.html',
            domain = json.dumps(domain),
        )
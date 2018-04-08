# encoding:utf-8

"""
团伙分析handler
"""
import tornado.web
import json
from base_handler import BaseHandler

class IllegalOrgsHandler(BaseHandler):
    """首页控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        value  = self.get_argument('value','000000.com')
        source = self.get_argument('source','domain')
        self.render(
            'illegal_orgs.html',
            source = json.dumps(source),
            value = json.dumps(value)
        )
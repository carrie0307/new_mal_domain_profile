# encoding:utf-8

"""
内外链总览handler
"""
import tornado.web
import json
from models.web_results import QueryWebResults
from base_handler import BaseHandler

default_domain = '000033333.com'

class LinksTotalHandler(BaseHandler):
    """内外链总览控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        results = QueryWebResults().get_links_info(domain)
        links_enter_num = results['links_enter']['num']
        links_outer_num = results['links_outer']['num']
        print domain
        print results
        self.render(
            'links_total.html',
            domain = json.dumps(domain),
            links_enter_num = links_enter_num,
            links_outer_num = links_outer_num,
            results = json.dumps(results)
        )
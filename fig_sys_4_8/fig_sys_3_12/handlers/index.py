# encoding:utf-8

"""
首页handler
"""
import tornado.web
from base_handler import BaseHandler
from models.MaltypeStatistic import MalTypeStatistic

class IndexHandler(BaseHandler):
    """首页控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        results = MalTypeStatistic().count_maltype()
        all = 0
        for value in results.values():
            all+=value
        results['all'] = all
        results =  [results['all'],results['gamble'],results['porno']]
        self.render(
            'index.html',
            results = results
        )

class RelativeORGHandler(BaseHandler):
    """相关机构控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        self.render(
            'relative_org.html'
        )
# encoding:utf-8

"""
非法域名全国地理位置归属统计handler
"""
import tornado.web
import json
from models.pos_locate import PosLocate
from base_handler import BaseHandler


class PosStatisticsHandler(BaseHandler):
    """非法域名全国地理位置归属统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        self.render(
            'pos_statistics.html'
        )

class PosStatisticsDataHandler(BaseHandler):
    """非法域名全国地理位置归属统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source = self.get_argument('source', 'reg_whois')
        results = PosLocate().get_domain_numinfo(source)
        map_result = []
        max_num = 0
        for res in results:
            row = dict(
                name=res['pos'],
                value=res['all']
            )
            if res['all'] > max_num:
                max_num = res['all']
            map_result.append(row)
        map_results = [map_result, max_num]
        results = [map_results,results]
        results = json.dumps(results)
        self.write(results)

class PosStaMapDataHandler(BaseHandler):
    """非法域名全国地理位置归属统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source = self.get_argument('source', 'reg_whois')
        pos_info = PosLocate().get_domain_numinfo(source)
        map_result = []
        max_num = 0
        for res in pos_info:
            row = dict(
                name=res['pos'],
                value=res['all']
            )
            if res['all'] > max_num:
                max_num = res['all']
            map_result.append(row)
        map_results = [map_result, max_num]
        map_results = json.dumps(map_results)
        self.write(map_results)
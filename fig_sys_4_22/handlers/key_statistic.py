# encoding:utf-8

"""
关键信息统计控制handler
"""
import tornado.web
import json
from models.key_statistic import KeyWhoisStatistic,IPStatistic
from models.pos_locate import PosLocate
from base_handler import BaseHandler

class KeyStatisticsGeneralHandler(BaseHandler):
    """关键信息总览统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source = self.get_argument('source', 'ip')
        if source == 'ip':
            data = IPStatistic().ip_baseinfo(-1)
        else:
            if source == 'registrar':
                source = 'sponsoring_registrar'
            data = KeyWhoisStatistic().keywhois(source, -1, has_all=True)
            if source == 'sponsoring_registrar':
                source = 'registrar'

        self.render(
            'general_list.html',
            source = json.dumps(source),
            data = json.dumps(data)
        )

class KeyStatisticsViewHandler(BaseHandler):
    """关键信息概览统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        topn = self.get_argument('topn', 10)
        self.render(
            'overview_list.html',
            topn = json.dumps(topn)
        )

# class KeyStatisticsViewDataHandler(BaseHandler):
#     """关键信息概览统计控制"""
#
#     @tornado.web.authenticated
#     def get(self):
#
#         self.get_authenticated()
#         topn = self.get_argument('topn', 10)
#         has_all = True
#         registrar_list = KeyWhoisStatistic().keywhois('sponsoring_registrar', topn,has_all=has_all)
#         reg_name_list = KeyWhoisStatistic().keywhois('reg_name', topn,has_all=has_all)
#         reg_phone_list = KeyWhoisStatistic().keywhois('reg_phone', topn,has_all=has_all)
#         reg_email_list = KeyWhoisStatistic().keywhois('reg_email', topn,has_all=has_all)
#         ip_list = IPStatistic().ip_baseinfo(topn)
#         ip_geo_list = PosLocate().get_domain_numinfo('ip')
#         data = [registrar_list,reg_name_list,reg_phone_list,reg_email_list,ip_list,ip_geo_list]
#         data = json.dumps(data)
#         self.write(data)

class KeyStatisticsViewDataHandler(BaseHandler):
    """关键信息概览统计控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        topn = self.get_argument('topn', 10)
        has_all = True
        registrar_list = KeyWhoisStatistic().keywhois('sponsoring_registrar', topn,has_all=has_all)
        reg_name_list = KeyWhoisStatistic().keywhois('reg_name', topn,has_all=has_all)
        reg_phone_list = KeyWhoisStatistic().keywhois('reg_phone', topn,has_all=has_all)
        reg_email_list = KeyWhoisStatistic().keywhois('reg_email', topn,has_all=has_all)
        ip_list = IPStatistic().ip_baseinfo(topn)
        ip_geo_list = PosLocate().get_domain_numinfo('ip')

        registrar_fig = [[],[]]
        for res in registrar_list:
            registrar_fig[0].append(res['sponsoring_registrar'])
            registrar_fig[1].append(res['domain_count'])

        reg_name_fig = [[], []]
        for res in reg_name_list:
            reg_name_fig[0].append(res['reg_name'])
            reg_name_fig[1].append(res['domain_count'])

        reg_phone_fig = [[], []]
        for res in reg_phone_list:
            reg_phone_fig[0].append(res['reg_phone'])
            reg_phone_fig[1].append(res['domain_count'])

        reg_email_fig = [[], []]
        for res in reg_email_list:
            reg_email_fig[0].append(res['reg_email'])
            reg_email_fig[1].append(res['domain_count'])

        ip_fig = [[], []]
        for res in ip_list:
            ip_fig[0].append(res['IP'])
            ip_fig[1].append(res['num'])

        data = [registrar_list, reg_name_list, reg_phone_list, reg_email_list, ip_list, ip_geo_list, registrar_fig, reg_name_fig, reg_phone_fig, reg_email_fig, ip_fig]
        data = json.dumps(data)
        self.write(data)
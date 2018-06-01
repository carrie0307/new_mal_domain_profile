# encoding:utf-8

"""
关联关系handler
"""
import tornado.web
import json
from base_handler import BaseHandler
from models.visual_analyse import Relative_domain_getter
from models.get_relative_reginfo import Relative_reginfo_getter

class VisualHandler(BaseHandler):
    """关联关系控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain','0518jx.com')
        relative_domain_getter = Relative_domain_getter(domain)
        graph_info, show_info = relative_domain_getter.get_relative_data()
        if show_info.get('reg_name_num') is None:
            show_info['reg_name_num']=0
        if show_info.get('reg_email_num') is None:
            show_info['reg_email_num']=0
        if show_info.get('reg_phone_num') is None:
            show_info['reg_phone_num']=0
        if show_info.get('links_domains_num') is None:
            show_info['links_domains_num']=0
        if show_info.get('enter_domains_num') is None:
            show_info['enter_domains_num']=0
        if show_info.get('cname_domains_num') is None:
            show_info['cname_domains_num']=0
        keys = show_info.get('ip_info').keys()
        values = show_info.get('ip_info').values()
        values = 0 if len(values)==0 else(sum(values))
        total = len(graph_info['links'])
        show_info = [
            show_info.get('reg_name'),
            show_info.get('reg_email'),
            show_info.get('reg_phone'),
            '/'.join(keys),
            show_info.get('reg_name_num'),
            show_info.get('reg_email_num'),
            show_info.get('reg_phone_num'),
            values,
            show_info.get('enter_domains_num'),
            show_info.get('links_domains_num'),
            show_info['cname_domains_num'],
            total
                     ]
        self.render(
            'visual.html',
            domain = domain,
            graph_info = json.dumps(graph_info),
            show_info = json.dumps(show_info)
        )

class GroupHandler(BaseHandler):
    """团伙关系控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain','0518jx.com')
        relative_reginfo_getter = Relative_reginfo_getter(domain)
        graph_info, show_info = relative_reginfo_getter.get_relative_data()
        reg_name_info = []
        reg_phone_info = []
        reg_email_info = []
        for dt in show_info['reg_name']:
            reg_name_info.append(["注册者:",dt['reg_name'],"关联域名数量:",dt['conn_dm_num']])
        for dt in show_info['reg_phone']:
            reg_phone_info.append(["注册电话:",dt['reg_phone'],"关联域名数量:", dt['conn_dm_num']])
        for dt in show_info['reg_email']:
            reg_email_info.append(["注册邮箱:",dt['reg_email'],"关联域名数量:",dt['conn_dm_num']])
        show_info = reg_name_info+reg_phone_info+reg_email_info
        self.render(
            'group.html',
            domain=domain,
            graph_info=json.dumps(graph_info),
            show_info=json.dumps(show_info)
        )
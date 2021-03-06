# encoding:utf-8

"""
IP历史状态探测handler
"""
import tornado.web
import json
import requests
from base_handler import BaseHandler
from models.get_ip_history import IP_history
from models.web_results import QueryWebResults

URL = 'http://10.246.24.57:5555'
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
        res.reverse()
        self.write(json.dumps(res))

# class WhoisHistoryHandler(BaseHandler):
#     """IP历史状态探测控制"""
#
#     @tornado.web.authenticated
#     def get(self):
#
#         self.get_authenticated()
#         domain = self.get_argument('domain', default_domain)
#         self.render(
#             'whois_history.html',
#             domain = json.dumps(domain),
#         )

class ContentHistoryHandler(BaseHandler):
    """页面内容历史控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        data = QueryWebResults().get_web_baseinfo(domain, query_all=True)
        results = []
        for content_analyse_results in data:
            if content_analyse_results['cur_url'] is not None and content_analyse_results['cur_url'] != '':
                analyse_results = [
                    ["页面标题", content_analyse_results['title']],
                    ["探测时间", content_analyse_results['detect_time'].split(".")[0]],
                    ["重定向域名", content_analyse_results['cur_url']],
                    ["页面描述", content_analyse_results['meta']],
                ]
            else:
                analyse_results = [
                    ["页面标题", content_analyse_results['title']],
                    ["探测时间", content_analyse_results['detect_time'].split(".")[0]],
                    ["页面描述", content_analyse_results['meta']],
                ]
            shot_path = content_analyse_results['shot_path']
            result = {
                "analyse_results": analyse_results,
                "shot_path": shot_path
            }
            results.append(result)

        results = json.dumps(results)
        self.render(
            'content_history.html',
            domain = json.dumps(domain),
            res = results
        )

class WhoisHistoryHandler(BaseHandler):
    """IP历史状态探测控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain', default_domain)
        cmp_url = URL + '/domain_resources/domain_whois/history/cmp/' + domain
        cmp_results = requests.get(cmp_url).json()
        print cmp_results

        whowas_res = {}
        for data in cmp_results:
            time_stamp = data['time_stamp']
            whowas_url = URL + '/domain_resources/domain_whois/history/' + domain + '/'+ time_stamp[0:10] + '%20' + time_stamp[11:19]
            res = requests.get(whowas_url).json()
            whowas_res[time_stamp]=res

        print whowas_res

        self.render(
                    'whois_history.html',
                    domain = json.dumps(domain),
                    cmp_results = json.dumps(cmp_results),
                    whowas_res = json.dumps(whowas_res)
                )
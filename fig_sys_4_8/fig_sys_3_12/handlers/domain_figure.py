# encoding:utf-8

"""
域名画像handler
"""
import tornado.web
import json
from base_handler import BaseHandler
from  models.general_list import QueryDomainGeneralInfo
from models.detect_results import QueryDetectResut
from models.analyse import IP_data_getter,Whois_info_getter,ICP_data_getter
from models.pos_locate import PosLocate
from models.web_results import QueryWebResults
from models.get_ip_new import newIP_data_getter


default_domain = '000033333.com'
class DomainFigureHandler(BaseHandler):
    """域名画像控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        baseinfo = QueryDomainGeneralInfo().get_baseinfo_bydomain(domain)
        baseinfo =  [baseinfo['domain'],baseinfo['dm_type'],baseinfo['http_code'],baseinfo['update_time']]
        detect_results = QueryDetectResut().get_detect_results(domain)
        ip_analyse_results = newIP_data_getter(domain).get_data()
        other_res = ip_analyse_results['other_dns_rr']
        CNAME = other_res['cname']
        if CNAME:
            CNAME.insert(0, "CNAME记录1")
            ip_analyse_results['other_dns_rr']['cname'] = [CNAME]

        NS = other_res['ns']
        if NS:
            NS.insert(0, "NS记录1")
            ip_analyse_results['other_dns_rr']['ns'] = [NS]

        TXT = other_res['txt']
        if TXT:
            TXT.insert(0, "TXT记录1")
            ip_analyse_results['other_dns_rr']['txt'] = [TXT]

        MX = other_res['mx']
        if MX:
            # MX_results = [['优先级', '交换域名']]
            MX_results = []
            for ms in MX:
                res = [value for value in ms.values()]
                MX_results.append(res)
            ip_analyse_results['other_dns_rr']['mx'] = MX_results



        SOA = other_res['soa']

        if SOA:
            # SOA_results = [['NS','负责人邮箱','序列号','刷新时间间隔','重试时间间隔','过期时间','生存时间']]
            # SOA_results = [['负责人邮箱', '重试时间间隔', 'NS', '生存时间', '刷新时间间隔', '过期时间', '序列号']]
            SOA_results = []
            for soa in SOA:
                res = [value for value in soa.values()]
                SOA_results.append(res)
            ip_analyse_results['other_dns_rr']['soa'] = SOA_results
        # ip_analyse_results = IP_data_getter(domain).get_ip_info()
        self.render(
            'domain_figure.html',
            domain=json.dumps(domain),
            baseinfo = json.dumps(baseinfo),
            detect_results = json.dumps(detect_results),
            analyse_results=json.dumps(ip_analyse_results)
        )

class ALLAnalyseDataHandler(BaseHandler):
    """域名画像控制"""
    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        baseinfo = QueryDomainGeneralInfo().get_baseinfo_bydomain(domain)
        baseinfo =  [baseinfo['domain'],baseinfo['dm_type'],baseinfo['http_code'],baseinfo['update_time']]
        detect_results = QueryDetectResut().get_detect_results(domain)
        ip_analyse_results = newIP_data_getter(domain).get_data()
        other_res = ip_analyse_results['other_dns_rr']
        CNAME = other_res['cname']
        if CNAME:
            CNAME.insert(0, "CNAME记录1")
            ip_analyse_results['other_dns_rr']['cname'] = [CNAME]

        NS = other_res['ns']
        if NS:
            NS.insert(0, "NS记录1")
            ip_analyse_results['other_dns_rr']['ns'] = [NS]

        TXT = other_res['txt']
        if TXT:
            TXT.insert(0, "TXT记录1")
            ip_analyse_results['other_dns_rr']['txt'] = [TXT]

        MX = other_res['mx']
        if MX:
            # MX_results = [['优先级', '交换域名']]
            MX_results = []
            for ms in MX:
                res = [value for value in ms.values()]
                MX_results.append(res)
            ip_analyse_results['other_dns_rr']['mx'] = MX_results



        SOA = other_res['soa']

        if SOA:
            # SOA_results = [['NS','负责人邮箱','序列号','刷新时间间隔','重试时间间隔','过期时间','生存时间']]
            # SOA_results = [['负责人邮箱', '重试时间间隔', 'NS', '生存时间', '刷新时间间隔', '过期时间', '序列号']]
            SOA_results = []
            for soa in SOA:
                res = [value for value in soa.values()]
                SOA_results.append(res)
            ip_analyse_results['other_dns_rr']['soa'] = SOA_results
        analyse_results=dict(
            baseinfo=baseinfo,
            detect_results=detect_results,
            analyse_results=ip_analyse_results
        )
        self.write(json.dumps(analyse_results))

class WHOISAnalyseDataHandler(BaseHandler):
    """域名画像控制"""
    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        whois_analyse_results = Whois_info_getter(domain).get_whois_info()
        table_content = []
        table_content.append(["注册者", whois_analyse_results['table_content']['reg_name']])
        table_content.append(["注册商", whois_analyse_results['table_content']['sponsoring_registrar']])
        table_content.append(["注册时间", whois_analyse_results['table_content']['creation_date']])
        table_content.append(["到期时间", whois_analyse_results['table_content']['expiration_date']])
        table_content.append(["更新时间", whois_analyse_results['table_content']['update_date']])
        table_content.append(["探测时间", whois_analyse_results['table_content']['insert_time']])
        table_content.append(["注册邮箱", whois_analyse_results['table_content']['reg_email']])
        table_content.append(["注册邮编", whois_analyse_results['table_content']['postal_code'],whois_analyse_results['table_content']['reg_postal_verify']])
        table_content.append(["注册电话", whois_analyse_results['table_content']['reg_phone'],whois_analyse_results['table_content']['reg_phone_verify']])
        table_content.append(["国家", whois_analyse_results['table_content']['country_code'],whois_analyse_results['table_content']['reg_whois_country']])
        table_content.append(["省份", whois_analyse_results['table_content']['province'],whois_analyse_results['table_content']['reg_whois_province']])
        table_content.append(["市区", whois_analyse_results['table_content']['city'],whois_analyse_results['table_content']['reg_whois_city']])
        table_content.append(["街道", whois_analyse_results['table_content']['street'],whois_analyse_results['table_content']['reg_whois_street']])
        table_content.append(["历史注册信息","<a href='/'>点击查看</a>"])
        whois_analyse_results['table_content'] = table_content
        self.write(json.dumps(whois_analyse_results))

class IPAnalyseDataHandler(BaseHandler):
    """域名画像控制"""
    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        # ip_analyse_results = IP_data_getter(domain).get_ip_info()
        ip_analyse_results = newIP_data_getter(domain).get_data()
        other_res = ip_analyse_results['other_dns_rr']
        CNAME = other_res['cname']
        if CNAME:
            CNAME.insert(0, "CNAME记录1")
            ip_analyse_results['other_dns_rr']['cname'] = [CNAME]

        NS = other_res['ns']
        if NS:
            NS.insert(0, "NS记录1")
            ip_analyse_results['other_dns_rr']['ns'] = [NS]

        TXT = other_res['txt']
        if TXT:
            TXT.insert(0, "TXT记录1")
            ip_analyse_results['other_dns_rr']['txt'] = [TXT]

        MX = other_res['mx']
        if MX:
            # MX_results = [['优先级', '交换域名']]
            MX_results = []
            for ms in MX:
                res = [value for value in ms.values()]
                MX_results.append(res)
            ip_analyse_results['other_dns_rr']['mx'] = MX_results



        SOA = other_res['soa']

        if SOA:
            # SOA_results = [['NS','负责人邮箱','序列号','刷新时间间隔','重试时间间隔','过期时间','生存时间']]
            # SOA_results = [['负责人邮箱', '重试时间间隔', 'NS', '生存时间', '刷新时间间隔', '过期时间', '序列号']]
            SOA_results = []
            for soa in SOA:
                res = [value for value in soa.values()]
                SOA_results.append(res)
            ip_analyse_results['other_dns_rr']['soa'] = SOA_results


        self.write(json.dumps(ip_analyse_results))

class ICPAnalyseDataHandler(BaseHandler):
    """域名画像控制"""
    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        icp_analyse_results = ICP_data_getter(domain).get_icp_info()
        analyse_results = []
        for res in icp_analyse_results:
            analyse_results.append([res['domain'],res['auth_icp'],res['page_icp'],res['icp_result'],res['ct']])
        self.write(json.dumps(analyse_results))

class PosAnalyseDataHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        pos_analyse_results = PosLocate().get_all_pos(domain)

        print pos_analyse_results

        results_1 = {'reg_phone_src': pos_analyse_results['reg_phone_src'],
              'reg_postal_src': pos_analyse_results['reg_postal_src'],
              'reg_whois_src': pos_analyse_results['reg_whois_src']}
        results_2 = {'page_icp_src': pos_analyse_results['page_icp_src'],
              'auth_icp_src': pos_analyse_results['auth_icp_src']}

        results_3 =  pos_analyse_results['ip_src']
        ip_results = []
        if len(results_3):
            for ip_res in results_3:
                res = [value for value in ip_res.values()]
                res.insert(0, "域名服务ip")
                ip_results.append(res)
        else:
            ip_results.append(["域名服务ip", "--", " ", " "])



        analyse_results = []
        icp_results = []
        map_data = []
        pos = set()
        poss = {}
        for key,value in results_1.iteritems():
            if value is None or value=="":
                val = 0
            else:
                val=1
            if not poss.get(value['concrete_pos']):
                poss[value['concrete_pos']]=val
            else:
                poss[value['concrete_pos']] = poss[value['concrete_pos']]+1

            pos.add(value['concrete_pos'])
            if key=="reg_phone_src":
                analyse_results.append(["注册电话",value['src'],value['concrete_pos'],value['pos']])
            elif key=="reg_postal_src":
                analyse_results.append(["注册邮编",value['src'],value['concrete_pos'],value['pos']])
            elif key=="reg_whois_src":
                analyse_results.append(["注册人地址",value['src'],value['concrete_pos'],value['pos']])


        for key, value in results_2.iteritems():
            if key=="page_icp_src":
                icp_results.append(["页面ICP备案",value['src'],value['concrete_pos'],value['pos']])
            elif key=="auth_icp_src":
                icp_results.append(["权威ICP备案",value['src'],value['concrete_pos'],value['pos']])
            # elif key=="ip_src":
            #     ip_icp_results.append(["域名服务ip",value['src'],value['concrete_pos'],value['pos']])

        for key,value in poss.iteritems():
            map_data.append(
                dict(
                    name=key,
                    value = value
                )
            )
        max_num = max(poss.values())
        if max_num == 1:
            rate = "不一致"
        elif max_num == 2:
            rate = "不完全一致"
        elif max_num == 3:
            rate = "完全一致"
        # rate =  max_num*1.0/3
        print rate
        map_data = [map_data,max_num]
        self.write(json.dumps([map_data,analyse_results,rate,icp_results,ip_results]))

class LinksAnalyseDataHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        links_analyse_results = QueryWebResults().get_links_baseinfo(domain)
        analyse_results = [
            ["链入站点数",links_analyse_results['num'][0]],
            ["链出站点数",links_analyse_results['num'][1]],
            ["非法链入站点数",links_analyse_results['num'][2]],
            ["合法链入站点数",links_analyse_results['num'][3]],
            ["內链数",links_analyse_results['num'][4]],
            ["外链数",links_analyse_results['num'][5]],
            ["暗链数", links_analyse_results['num'][6]]
        ]
        fig_data = dict(
            xdata = ["链入站点数/链入域名数","外链数/外链域名数","站点数/外链数"],
            ydata = links_analyse_results['rate']
        )

        self.write(json.dumps([analyse_results,fig_data]))

class ContentAnalyseDataHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        domain = self.get_argument('domain',default_domain)
        content_analyse_results = QueryWebResults().get_web_baseinfo(domain,query_all=False)
        analyse_results = [
            ["页面标题", content_analyse_results['title']],
            ["重定向域名", content_analyse_results['redirect_domain']],
            ["页面描述", content_analyse_results['meta']],
            ["探测时间", content_analyse_results['detect_time']],
        ]
        shot_path = content_analyse_results['shot_path']

        self.write(json.dumps([analyse_results,shot_path]))
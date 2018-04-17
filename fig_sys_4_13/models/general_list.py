# -*- coding: utf-8 -*-

from Base import Base

class QueryDomainGeneralInfo(Base):
    """
    域名总体信息查询
    """
    def __init__(self):
        Base.__init__(self)

    def get_general_list(self,source='general',source_value='',maltype=None):
        """
        域名信息表:域名、域名类型、站点状态、IP数量、探测时间、服务ip,ip归属地、合法链入数、非法链入数、外链数、內链数、暗链数
        :param source: 不输入/ip/sponsoring_registrar/reg_email/reg_phone/reg_name
                        (总体域名信息/根据ip、注册商、注册邮箱、注册电话、注册者反查、地理位置)
        :param source_value: 反查源的值
        :return: [{
            'domain':域名,
            'update_time': 探测时间,
            'IP': 服务ip,
            'inner_links_num': 內链数,
            'legal_enter_num': 合法链入数,
            'outer_links_num': 外链数,
            'IP_num': IP数量,
            'dm_type': 域名类型,
            'hidden_links_num':暗链数 ,
            'mal_enter_num':非法链入数,
            'http_code': 站点状态,
            'IP_geo': ip归属地
            },{...},...,{...}]
        """
        limit_num = ' limit 100'
        if source == 'general':
            sql = "select * from domain_general_list"
            if maltype:
                sql = sql+" where dm_type='%s'"%maltype
            sql = sql + limit_num
            res = self.mysql_db.query(sql)
        elif source == 'ip':
            sql = 'select dg.* from domain_general_list dg join domain_ip_relationship di on dg.domain=di.domain ' \
                  ' where di.ip=%s'
            if maltype:
                sql = sql + " and dg.dm_type='%s'" % maltype
            sql = sql + limit_num
            res = self.mysql_db.query(sql,source_value)
        elif source in ['sponsoring_registrar','reg_email','reg_phone','reg_name']:
            sql = 'select dg.* from domain_general_list dg join domain_whois dw on dg.domain=dw.domain ' \
                  ' where dw.'+source+'=%s'
            if maltype:
                sql = sql + " and dg.dm_type='%s'" % maltype
            sql = sql + limit_num
            res = self.mysql_db.query(sql, source_value)
        elif source == 'pos':
            sql1 = "select dg.* from domain_general_list dg, domain_locate dw, domain_icp d_icp\
                    where (dw.reg_whois_province = '%s' or dw.reg_phone_province = '%s' or dw.reg_postal_province = '%s'\
                    or d_icp.icp_province = '%s') and (dg.domain = dw.domain and dw.domain = d_icp.domain)" %(source_value,source_value,source_value,source_value)
            sql2 = "select a.* from domain_general_list a join domain_ip_relationship b on a.domain = b.domain" \
                  " where b.ip_province = %s"
            if maltype:
                sql1 = sql1 + " and dg.dm_type='%s'" % maltype
                sql2 = sql2 + " and a.dm_type='%s'" % maltype
            sql1 = sql1 + limit_num
            sql2 = sql2 + limit_num
            res1 = self.mysql_db.query(sql1)
            res2 = self.mysql_db.query(sql2, source_value)
            res =  res1+res2
        else:
            print "无该项查询"
            res = []

        if len(res)!=0:
            results = []
            if source == 'general':
                for rs in res:
                    rs['update_time'] = str(rs['update_time'])
                    results.append(rs)
            else:
                domains = []
                for rs in res:
                    domain = rs['domain']
                    if domain in domains:
                        continue
                    else:
                        domains.append(domain)
                    new_rs = {}
                    new_rs['domain'] = rs['domain']
                    new_rs['dm_type'] = rs['dm_type']
                    if isinstance(rs['http_code'],str) and rs['http_code']!='':
                        if rs['http_code'][0] in ['2','3']:
                            new_rs['web_status'] = '可访问'
                        else:
                            new_rs['web_status'] = '不可访问'
                    else:
                        new_rs['web_status'] = '未检测'
                    new_rs['server_ip'] = rs['IP']
                    new_rs['ip_num'] = rs['IP_num']
                    new_rs['ip_geo'] = rs['IP_geo']
                    new_rs['detect_time'] = str(rs['update_time'])
                    new_rs['enter_num'] = rs['legal_enter_num'] + rs['mal_enter_num']
                    new_rs['outer_num'] = rs['outer_links_num'] + rs['hidden_links_num']
                    results.append(new_rs)
        else:
            results = res

        return results

    def get_baseinfo_bydomain(self,domain):

        limit_num = ' limit 100'
        sql = "select domain,dm_type,http_code,update_time from domain_general_list where domain=%s"+limit_num
        result = self.mysql_db.get(sql, domain)

        print result
        print "lallalalallal=--------"

        result['update_time'] = str(result['update_time'])
        if (isinstance(result['http_code'], unicode) or isinstance(result['http_code'], str))and result['http_code'] != '':
            if result['http_code'][0]=='2':
                result['http_code'] = '可访问'+ ' ('+result['http_code']+')'
            elif result['http_code'][0] == '3':
                result['http_code'] = '重定向'+ ' ('+result['http_code']+')'
            else:
                result['http_code'] = '不可访问'+ ' ('+result['http_code']+')'
        else:
            result['http_code'] = '未检测'
        return result

if __name__ == "__main__":
    qdg = QueryDomainGeneralInfo()
    # print qdg.get_general_list()
    # print qdg.get_general_list(source='reg_name',source_value='yangbo')
    # print qdg.get_general_list(source='reg_email', source_value='5343@163.com')
    # print qdg.get_general_list(source='reg_phone', source_value='+86.13811119831')
    # print qdg.get_general_list(source='sponsoring_registrar', source_value='1API GmbH')
    # print qdg.get_general_list(source='ip', source_value='52.73.207.56')
    # print qdg.get_general_list(source='sponsoring_registrar', source_value='1API GmbH',maltype="非法赌博")
    # print QueryDomainGeneralInfo().get_baseinfo_bydomain('000000.in')
    # print QueryDomainGeneralInfo().get_baseinfo_bydomain('0000779.com')
    print QueryDomainGeneralInfo().get_baseinfo_bydomain('0371tk.com')

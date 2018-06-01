# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arrow
import datetime
import MySQLdb
from Base import Base

class DomainAnalyseInfo(Base):
    """
    分析
    """
    def __init__(self):
        Base.__init__(self)


class ICP_data_getter(Base):

    def __init__(self,domain):
        self.domain = domain
        Base.__init__(self)

    def get_icp_result(self,auth_icp,page_icp):

        icp_result = "正常ICP"
        if auth_icp=='--':
            if page_icp=='--':
                icp_result = "无ICP"
            else:
                icp_result = "异常ICP"
        else:
            if page_icp in ['--','-1']:
                icp_result = "可疑ICP"
            elif page_icp!=auth_icp:
                icp_result = "虚假ICP"
        return icp_result

    def get_icp_info(self):

        sql = "select domain,auth_icp,page_icp from domain_icp where domain=%s"
        res = self.mysql_db.get(sql,self.domain)
        auth_icp = res['auth_icp']
        page_icp = res['page_icp']
        icp_result = self.get_icp_result(auth_icp,page_icp)
        res['icp_result']=icp_result
        ct = 0
        if icp_result == "异常ICP" and page_icp!='-1':
            sql = "select domain,auth_icp,page_icp from domain_icp where page_icp=%s"
            results = self.mysql_db.query(sql, page_icp)
            ct = len(results)-1
            res['ct'] = ct
            rows = [res]
            if ct>0:
                for rs in results:
                    if rs['domain']!=self.domain:
                        rs['ct'] = ct
                        rs['icp_result'] = self.get_icp_result(rs['auth_icp'], rs['page_icp'])
                        rows.append(rs)
        else:
            res['ct'] = ct
            rows = [res]

        return rows

class IP_data_getter(Base):

    def __init__(self,domain):
        self.domain = domain
        Base.__init__(self)

    def deal_geo_info(self,country,region,city):
        """
        组装完整的地理位置信息
        """
        geo = country
        if country == '香港' or country == '台湾' or country == '内网IP':
            return geo
        elif region != '0':
            geo = geo + '-' + region
        if city != '0' and city != region:
            geo = geo + '-' + city
        return geo


    def deal_state_info(self,state):
        """
        功能：对80端口状态信息进行处理
        """
        if state == 'open':
            return '80端口-开放'
        elif state == 'closed':
            return '80端口-关闭'
        else:
            # 对应filter和没有scan字段的情况(0)
            return '无法探测到状态'


    def get_table_ip_info(self):
        '''
        功能： 获取表格中所需要的ip信息
        '''
        sql = "SELECT a.IP,a.last_detect_time,b.state80,b.country,b.region,b.city,b.oper,b.ASN,b.AS_OWNER\
        FROM (SELECT domain_ip_relationship.IP,domain_ip_relationship.last_detect_time\
        FROM domain_ip_relationship WHERE domain = '%s') AS a\
        LEFT JOIN ip_general_list as b ON a.IP = b.IP;" %(self.domain)

        fetch_data = self.mysql_db.query(sql)
        table_ip_info = []

        if fetch_data:
            for item in fetch_data:

                ip,last_detect_time,state,country,region,city,oper,asn,as_owner = item

                item['geo'] = self.deal_geo_info(item['country'],item['region'],item['city'])
                del item['country']
                del item['region']
                del item['city']

                item['state80'] = self.deal_state_info(item['state80'])
                table_ip_info.append(item)

        return table_ip_info


    def get_domain_ip_num(self):
        '''
        功能： 获取曾给该域名提供服务的不重复的ip数量(the num of dinstinct IPs that hosted the domain ever)
        '''
        sql = "SELECT IP_num FROM domain_general_list WHERE domain = '%s';" %(self.domain)
        fetch_data = self.mysql_db.query(sql)
        if fetch_data:
            ip_num = int(fetch_data[0]['IP_num'])
            return ip_num
        else:
            print '无此域名记录'
            return


    def get_ip_change_frequency(self):
        '''
        功能： 获取ip变化频率数值
        '''
        return ''


    def get_ip_info(self):
        '''
        功能：获取ip分析部分所需数据
        return ip_info: {ip_num:ip数量,ip_change_frequency:ip变化频率，table_info:[{},{}] # 表格中所需数据，每个元素为一个字典，该字典对应表中的一行}
        eg. {
        'ip_num': 2,
         'table_info': [
         {'state80': '80端口开放', 
         'IP': u'52.73.207.56',
          'last_detect_time': u'2018-01-09 20:43:25', 
          'AS_OWNER': u'AMAZON-AES - Amazon.com',
           'ASN': u'14618',
            'geo': u'中国山东',
             'oper': u'电信'
             }}], 'ip_change_frequency': '---'}
        '''
        ip_info = {'ip_num':0,'ip_change_frequency':'', 'table_info':[],}
        ip_num = self.get_domain_ip_num()
        ip_info['ip_num'] = ip_num
        if ip_info['ip_num'] == 0:
            return ip_info
        elif ip_info['ip_num'] == None:
            return ip_info
        else:# 正常存在到ip的情况
            ip_info['table_info'] = self.get_table_ip_info()
            ip_info['ip_change_frequency'] = self.get_ip_change_frequency()
        ip_info['table_info']=self.add_seq_num(ip_info['table_info'])

        return ip_info

class Whois_info_getter(Base):

    def __init__(self,domain):
        self.domain = domain
        Base.__init__(self)

    def get_whois_info(self):
        '''
        功能：获取域名的whois相关信息
        param: domain: 要获取信息的域名
        return: res= {'talble_content':表格里显示的信息，'tag':标签中显示的信息(关联数量和生命周期)}
        '''

        # 获取基础whois信息
        whois_info = self.get_whois_key_info()
        if whois_info:
            reg_name,reg_email,reg_phone,sponsoring_registrar = whois_info['reg_name'],whois_info['reg_email'],whois_info['reg_phone'],whois_info['sponsoring_registrar']
            creation_date,expiration_date,update_date,insert_time = whois_info['creation_date'],whois_info['expiration_date'],whois_info['update_date'],whois_info['insert_time']
            insert_time = self.datetime2string(insert_time)
        else:
            return '无该域名whois信息'

        # 获取关联域名数量
        reg_name,reg_name_num,reg_email,reg_email_num,reg_phone,reg_phone_num = self.get_reg_dm_num(reg_name,reg_email,reg_phone)

        # 计算生命周期
        live_period = self.count_life_perios(creation_date,expiration_date)

        table_content = {}
        table_content = {'reg_name':whois_info['reg_name'],'reg_email':reg_email,'reg_phone':reg_phone,\
                         'sponsoring_registrar':sponsoring_registrar,'creation_date':creation_date,\
                         'expiration_date':expiration_date,'update_date':update_date,'insert_time':insert_time
                        }
        # 获取地理位置，验证电话，邮编
        self.get_whois_locate(table_content)

        # 整合结果
        res = {'table_content':table_content,
                'tag':{'reg_name_num':reg_name_num,'reg_email_num':reg_email_num,'reg_phone_num':reg_phone_num,'live_period':live_period}
              }
        return res


    def get_whois_key_info(self):
        '''
        功能：从domain_whois中获取所需数据
        param: domain: 要查询的域名
        return: [reg_name,reg_email,reg_phone,sponsoring_registrar,creation_date,expiration_date,update_date,insert_time] whis表中查到的信息
        return: [] 查不到该域名注册信息
        '''
        sql = "SELECT reg_name,reg_email,reg_phone,sponsoring_registrar,creation_date,expiration_date,update_date,insert_time\
               FROM domain_whois\
               WHERE domain = '%s';" %(self.domain)
        fetch_data = self.mysql_db.query(sql)
        if fetch_data:
            # print  fetch_data[0]
            return fetch_data[0]
        else:
            return []


    def datetime2string(self,date_time):
        '''
        将datetime转化为字符串
        '''
        if isinstance(date_time,datetime.datetime):
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return date_time


    def get_whois_locate(self,table_content):
        '''
        功能：获取whois信息中的地理位置和邮编信息
        param: domain: 要获取信息的域名
        return: geo:   whois中原始的地理位置信息
        return: postal_code:   whois中的邮编
        '''

        table_content['country_code'],table_content['city'],table_content['street'],table_content['province']= '','','',''
        table_content['reg_whois_country'],table_content['reg_whois_province'],table_content['reg_whois_city'],table_content['reg_whois_street'] = '','','',''
        table_content['postal_code'] = ''
        table_content['reg_phone_verify'] = ''


        sql = "SELECT reg_whois_country,reg_whois_province,reg_whois_city,reg_whois_street,\
                      reg_postal_country,reg_postal_province,reg_postal_city,reg_phone_country,reg_phone\
                      reg_phone_province,reg_phone_city,province,country_code,city,street,postal_code\
                FROM domain_locate WHERE domain = '%s';" %(self.domain)
        fetch_data = self.mysql_db.query(sql)

        if fetch_data:
            fetch_data = fetch_data[0]

            for key in ['reg_whois_country','reg_whois_province','reg_whois_city','reg_whois_street',\
                        'province','country_code','city','street','postal_code']:
                table_content[key] = fetch_data[key] if fetch_data[key] != 'None' else ''

            # print table_content
            # print table_content['reg_phone']
            # print table_content['postal_code']
            if table_content['reg_phone'] != '':
                if fetch_data['reg_phone_country'] == '外国':
                    table_content['reg_phone_verify'] = '合格'
                elif fetch_data['reg_phone_country'] != 'None' and fetch_data['reg_phone_province'] != 'None' and fetch_data['reg_phone_city'] != 'None':
                    table_content['reg_phone_verify'] = '合格'
                else:
                    table_content['reg_phone_verify'] = '不合格'
            else:
                table_content['reg_phone_verify'] = ''

            if  table_content['postal_code'] and table_content['postal_code'] != 'None':#
                if fetch_data['reg_postal_country'] == '外国':
                    table_content['reg_postal_verify'] = '合格'
                elif fetch_data['reg_postal_country'] != 'None' and fetch_data['reg_postal_province'] != 'None' and fetch_data['reg_postal_city'] != 'None':
                    table_content['reg_postal_verify'] = '合格'
                else:
                    table_content['reg_postal_verify'] = '不合格'
            else:
                table_content['reg_postal_verify'] = ''


    def get_reg_dm_num(self,reg_name,reg_email,reg_phone):
        '''
        功能： 获取注册信息关联的域名数量
        param: reg_name   注册姓名
        param: reg_email  注册邮箱
        param: reg_phone  注册电话
        注：1. 查不到该注册信息对应数量，则返回数量为'--'
           2.  注册信息如果为空，则返回'*'
        '''
        reg_name_num,reg_email_num,reg_phone_num = '*','*','*'

        if reg_name != '':
            reg_name = MySQLdb.escape_string(reg_name)
            sql = "SELECT domain_count FROM reg_info WHERE item = '%s';" %(reg_name)
            fetch_data = self.mysql_db.query(sql)
            reg_name_num = int(fetch_data[0]['domain_count']) if fetch_data else '--'
        if reg_email != '':
            reg_email = MySQLdb.escape_string(reg_email)
            sql = "SELECT domain_count FROM reg_info WHERE item = '%s';" %(reg_email)
            fetch_data = self.mysql_db.query(sql)
            reg_email_num = int(fetch_data[0]['domain_count']) if fetch_data else '--'
        if reg_phone != '':
            reg_phone = MySQLdb.escape_string(reg_phone)
            sql = "SELECT domain_count FROM reg_info WHERE item = '%s';" %(reg_phone)
            fetch_data = self.mysql_db.query(sql)
            reg_phone_num = int(fetch_data[0]['domain_count']) if fetch_data else '--'

        return reg_name,reg_name_num,reg_email,reg_email_num,reg_phone,reg_phone_num


    def count_life_perios(self,creation_date,expiration_date):
        '''
        功能：根据注册日期和过期日期计算生存时间
        return: return_live[*** 天(约**年)] 当日期为空时，返回 ‘--’

        提取主体部分处理
        0558520.com  2016-11-17 T19:31:05Z
        0471web.com  3/9/2017 7:06:03 AM
        0555.in      15-May-2014 06:31:06 UTC
        0-5baby.com  2018-01-06 00:00:00

        ' '无法提取出主体年月日，但arrow可处理其全部
        0-craft.com  2017-11-18T06:08:09.00Z

        '''
        # print creation_date,expiration_date
        if creation_date == '' or expiration_date == '':
            return '---'

        # 只对时间的主体部分处理
        creation_date = creation_date.split(' ')[0]
        start = arrow.get(creation_date)

        expiration_date = expiration_date.split(' ')[0]
        end = arrow.get(expiration_date)

        # 天数
        live_period = (end-start).days
        # 转化为年
        live_years = round(live_period / 365,2)

        return_live = str(live_period) + ' days(约' + str(live_years) + '年)'
        return return_live

if __name__ == '__main__':
    # print Whois_info_getter('000000.com').get_whois_info()
    res=  Whois_info_getter('00000151.com').get_whois_info()
    print res
    for k,v in res['table_content'].iteritems():
        print k,v
    # print res['table_content']['update_date']
    # print res['table_content']['expiration_date:']
    # print res['table_content']['creation_date']
    # print res['table_content']['insert_time']
    # ip_data_getter = IP_data_getter('000000.in')
    # print ip_data_getter.get_ip_info()
    # print ICP_data_getter('00000z.com').get_icp_info()

# encoding:utf-8
import dns.resolver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..") # 回退到上一级目录
import database.mysql_operation
mysql_conn = database.mysql_operation.MysqlConn('10.245.146.43','root','platform','mal_domain_profile','utf8')

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['1.2.4.8']

"""地理位置相关"""
import ip2region.ip2Region
import ip2region.exec_ip2reg
searcher = ip2region.ip2Region.Ip2Region("ip2region/ip2region.db")

counter = 0


def get_domains():
    '''
    功能： 获取原ip和域名
    :return: [(ip,domain), (ip,domain), ...]
    '''
    domain_ip_list = []
    sql = "SELECT ip,domain FROM ip_reverse_new WHERE ip_detail is null;"
    fetch_data =list(mysql_conn.exec_readsql(sql))
    for item in fetch_data:
        domain_ip_list.append(item)
    return domain_ip_list


def get_IP_record(domain):
    '''
    功能： 获取A记录
    :param: domain: 待探测A记录的域名
    :return: ip_details: [ip1,ip2,...] flag:1  (当正常探测到IP时，返回IP列表和标志位1)
             ip_details: [exception_msg] flag:0 (当出现异常时，返回异常信息和标志位0)
    '''
    global resolver
    for _ in range(3):
        flag = 0 # 始终正常获取标志位
        ip_details = []
        try:
            resp_A = resolver.query(domain, 'A')
            resp_A.response.answer
            answers= [answer.to_text() for answer in resp_A.response.answer]
            '''
            当answers = [u'www.baidu.com. 557 IN CNAME www.a.shifen.com.', u'www.a.shifen.com. 44 IN A 220.181.111.188\nwww.a.shifen.com. 44 IN A 220.181.112.244']时，
            遍历到record.split(' ')[3] == 'A'时，record.split(' ')[4] == '220.181.111.188\nwww.a.shifen.com.'，
            因此用'\n'进行split处理，ip = record.split(' ')[4].split('\n')[0]
            如果没有cname，则用 '\n'分割后结果不变
            '''
            for record in answers:
                record = record.split(' ')
                if record[3] == 'A':
                    ip = record[4].split('\n')[0]
                    ip_details.append(ip)
            flag = 1
            break
        except dns.resolver.NoAnswer, e:
            ip_details.append('A Exception msg:NoAnswer')
        except dns.resolver.NXDOMAIN, e:
            ip_tmp_msg = 'A Exception msg:NXDOMAIN'
            ip_details.append('A Exception msg:NXDOMAIN')
        except dns.resolver.NoNameservers, e:
            ip_details.append('A Exception msg:NoNameserve')
        except dns.resolver.Timeout, e:
            ip_details.append('A Exception msg:Timeout')
        except:
            ip_details.append('A Exception msg:Unexcepted Errors')
    return ip_details,flag


def cmp_ip(ip_details,ip):
    '''
    功能：比对原IP是否在当前IP列表里
    '''
    if ip in ip_details:
        return 1
    else:
        return 0

def save_info(domain,ip_details,ip_cmp_flag,ip_geo_info):
    '''
    功能： 存储
    '''
    global counter
    sql = "UPDATE ip_reverse_new SET ip_detail = '%s',flag = %d, ip_geo_info = '%s'\
           WHERE domain = '%s';" %(ip_details,ip_cmp_flag,ip_geo_info, domain)
    exec_res = mysql_conn.exec_cudsql(sql)
    if exec_res:
        counter += 1
        # print "counter : " + str(counter)
        if counter == 100:
            mysql_conn.commit()
            counter = 0


if __name__ == '__main__':
    domain_ip_list = get_domains()
    for ip,domain in domain_ip_list:
        ip_details,flag = get_IP_record(domain)
        if flag:
            # 如果正常获取到了IP，则进行比对
            ip_cmp_flag = cmp_ip(ip_details,ip)
            # 进行IP地理位置解析
            ip_geo_list = []
            for cur_ip in ip_details:
                ip_geo_info = ip2region.exec_ip2reg.get_ip_geoinfo(searcher,cur_ip)
                ip_info = ip_geo_info['country'] + '-' + ip_geo_info['region'] + '-' + ip_geo_info['oper']
                ip_geo_list.append(ip_info)
            ip_geo_info = ';'.join(ip_geo_list)
        else:
            ip_cmp_flag = -1
            ip_geo_info = '---'
        ip_details = ';'.join(ip_details)
        print domain,ip_details,ip_cmp_flag,ip_geo_info
        save_info(domain,ip_details,ip_cmp_flag,ip_geo_info)
    mysql_conn.commit()

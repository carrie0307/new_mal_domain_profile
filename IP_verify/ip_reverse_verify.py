# encoding:utf-8
'''
    功能： 获取域名IP与地理位置，对学长给出的信息进行验证
'''
import dns.resolver
import Queue
import threading
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..") # 回退到上一级目录
import database.mysql_operation
mysql_conn = database.mysql_operation.MysqlConn('10.245.146.43','root','platform','mal_domain_profile','utf8')
table_name = 'ip_reverse_new2'

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['1.2.4.8']

"""地理位置相关"""
import ip2region.ip2Region
import ip2region.exec_ip2reg
searcher = ip2region.ip2Region.Ip2Region("ip2region/ip2region.db")

"""commit计数器"""
counter = 0

"""同步队列"""
domain_q = Queue.Queue()
res_q = Queue.Queue()

thread_num = 5



def get_domains():
    '''
    功能： 获取原ip和域名
    :return: [(ip,domain), (ip,domain), ...]
    '''
    global domain_q
    global table_name
    sql = "SELECT ip,domain FROM %s WHERE ip_flag = -2;" %(table_name)
    fetch_data =list(mysql_conn.exec_readsql(sql))
    for item in fetch_data:
        ip,domain = item
        domain_q.put([ip,domain])
    print '数据读取完成 ... '


def get_IP_record(domain):
    '''
    功能： 获取A记录
    :param: domain: 待探测A记录的域名
    :return: ip_details: [ip1,ip2,...] flag:1  (当正常探测到IP时，返回IP列表和标志位1)
             ip_details: [exception_msg] flag:0 (当出现异常时，返回异常信息和标志位0)
    '''
    global resolver
    for _ in range(3):
        flag = False # 标志是否正常完成了获取
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
            # 正常获取到了IP
            flag = True
            break
        except dns.resolver.NoAnswer, e:
            ip_details.append('A Record Exception msg:NoAnswer')
        except dns.resolver.NXDOMAIN, e:
            ip_tmp_msg = 'A Record Exception msg:NXDOMAIN'
            ip_details.append('A Record Exception msg:NXDOMAIN')
        except dns.resolver.NoNameservers, e:
            ip_details.append('A Record Exception msg:NoNameserve')
        except dns.resolver.Timeout, e:
            ip_details.append('A Record Exception msg:Timeout')
        except:
            ip_details.append('A Record Exception msg:Unexcepted Errors')
    return ip_details,flag


def cmp_ip_details(flag,ip_details,ip):
    '''
    功能：当前IP与原IP比对
    param: flag: 获取A记录所得flag
    param: ip_details: get_IP_record所得结果(当前IP集合)
    param: ip：从数据库读取的域名原IP
    ip_cmp_flag: 原IP与当前IP集合比对结果
                 ip_cmp_flag = 1,  原IP在当前IP集合中
                 ip_cmp_flag = 0,  原IP不在当前IP集合中
                 ip_cmp_flag = -1, 当前IP请求失败，无法进行比对
    country,province,city,oper: 当前对原IP进行地理位置解析结果
    '''
    if flag:
        # 如果正常获取到了IP，则进行比对
        ip_cmp_flag = cmp_ip(ip_details,ip)
    else:
        ip_cmp_flag = -1
    # 对原IP进行IP地理位置解析
    ip_geo_info = ip2region.exec_ip2reg.get_ip_geoinfo(searcher,ip)
    country,province,city,oper = ip_geo_info['country'],ip_geo_info['region'],ip_geo_info['city'],ip_geo_info['oper']
    return ip_cmp_flag,country,province,city,oper


def cmp_ip(ip_details,ip):
    '''
    功能：比对原IP是否在当前IP列表里
    '''
    if ip in ip_details:
        return 1
    else:
        return 0


def get_IP_record_handler():
    '''
    获取A记录并进行比对，将结果加入结果队列
    '''
    global domain_q
    global res_q
    while domain_q:
        ip,domain = domain_q.get(timeout = 100)
        # 获取A记录
        ip_details,flag = get_IP_record(domain)
        # 进行验证比对与IP地理位置信息获取
        ip_cmp_flag,country,province,city,oper = cmp_ip_details(flag,ip_details,ip)
        # 向结果队列中添加
        res_q.put([domain,ip_cmp_flag,country,province,city,oper])
    print '数据获取完成 ... '


def mysql_save_info():
    '''
    功能： 存储
    '''
    global counter
    global table_name
    while True:
        try:
            domain,ip_cmp_flag,country,province,city,oper = res_q.get(timeout = 150)
            insert_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print domain,ip_cmp_flag,country,province,city,oper
        except Queue.Empty:
            print 'mysql存储获取完成 ... '
            break
        # sql语句
        sql = "UPDATE %s SET ip_flag = %d, country = '%s',province = '%s',city = '%s',oper = '%s',\
            ip_verify_time = '%s'WHERE domain = '%s';" %(table_name,ip_cmp_flag,country,province,city,oper,insert_time,domain)
        exec_res = mysql_conn.exec_cudsql(sql)
        if exec_res:
            counter += 1
            # print "counter : " + str(counter)
            if counter == 100:
                mysql_conn.commit()
                counter = 0
    mysql_conn.commit()
    print 'mysql commit 全部完成 ... '


if __name__ == '__main__':
    get_domains()
    get_record_td = []
    for _ in range(thread_num):
        get_record_td.append(threading.Thread(target=get_IP_record_handler))
    for td in get_record_td:
        td.start()
    time.sleep(20)
    print 'save ip info ...\n'
    mysql_save_db_td = threading.Thread(target=mysql_save_info)
    mysql_save_db_td.start()
    mysql_save_db_td.join()
    print 'end:   ', time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

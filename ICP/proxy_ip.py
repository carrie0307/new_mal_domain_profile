# coding=utf-8
'''
    IP代理获取
    注意： 每次运行前，填写 订单号 和 每次获取IP数量
'''
import requests
import threading
import Queue
import time
raw_ip_proxy_q = Queue.Queue()
available_ip_proxy_q = Queue.Queue()

transaction_id = '138220909167713444'
get_proxy_num = 30

def get_raw_proxy_ip():
    '''
    获取原是IP
    '''
    global transaction_id,get_proxy_num
    global raw_ip_proxy_q
    # url = 'http://www.httpdaili.com/api.asp?ddbh=137505705110713444&noinfo=false&text=true$sl=5'
    url = "http://%s.standard.hutoudaili.com/?num=%d&area_type=1&style=2" %(transaction_id,get_proxy_num)
    content = requests.get(url).content
    ips = content.split('\n')
    for ip in ips:
        raw_ip_proxy_q.put(ip)


def whether_ip_available():
    '''
    测试IP可用性
    '''
    global available_ip_proxy_q
    while True:
        try:
            IP = raw_ip_proxy_q.get(timeout=120)
        except Queue.Empty:
            # 让这个线程始终存活着
            time.sleep(600)
        proxy = {'http': 'http://' + IP}
        try:
            res=requests.get("http://www.baidu.com",proxies=proxy,timeout=10)
            if res.content.find("百度一下")!=-1:
                available_ip_proxy_q.put(proxy)
                print proxy, '可用, cur_size:   ', available_ip_proxy_q.qsize()
        except:
            pass


def watch_ip_num():
    '''
    可用IP数量监控
    '''
    counter = 0
    global available_ip_proxy_q,raw_ip_proxy_q
    while True:
        if available_ip_proxy_q.qsize() < 12:
            get_raw_proxy_ip()
            print '再次获取代理IP...'
            # counter 标记进行了多少次获取
            counter = counter + 1
        else:
            print '当前可用代理数量：', str(available_ip_proxy_q.qsize())
            time.sleep(300)

def proxy_ip_general_run():
    get_raw_proxy_ip()
    verify_IP_td = []
    for _ in range(5):
        verify_IP_td.append(threading.Thread(target=whether_ip_available))
    for td in verify_IP_td:
        td.setDaemon(True)
    print '开始验证IP ... '
    for td in verify_IP_td:
        td.start()
    watch_ip_num_td = threading.Thread(target=watch_ip_num)
    watch_ip_num_td.setDaemon(True)
    watch_ip_num_td.start()


if __name__ == '__main__':
    get_raw_proxy_ip()
    # verify_IP_td = []
    # for _ in range(5):
    #     verify_IP_td.append(threading.Thread(target=whether_ip_available))
    # for td in verify_IP_td:
    #     td.setDaemon(True)
    # print '开始验证IP ... '
    # for td in verify_IP_td:
    #     td.start()
    # watch_ip_num_td = threading.Thread(target=watch_ip_num)
    # watch_ip_num_td.setDaemon(True)
    # watch_ip_num_td.start()
    # time.sleep(100)
    # print '开始获取... '
    # while True:
    #     proxy = available_ip_proxy_q.get()
    #     print proxy

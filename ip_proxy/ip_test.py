# encoding:utf-8
import requests

with open('ips.txt', 'r') as f:
    ips = f.read()
# ips = '202.100.83.139:80 120.77.254.116:3128'
print type(ips)
ips = ips.split('\n')

counter = 0
for i,ip in enumerate(ips):
    if ip:
        ip = ip.strip()
        print ip
        proxy = {'http': 'http://' + ip}
        # print "测试：" + str(IP) + "\n"
        try:
            res=requests.get("http://www.baidu.com",proxies=proxy,timeout=10)
            if res.content.find("百度一下")!=-1:
                msg = '可用...'
                counter = counter + 1
        except:
            msg = '不可用...'
            pass
        print i, ': ', ip, msg

print 'available counter :', counter

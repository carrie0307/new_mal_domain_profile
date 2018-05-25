# encoding:utf-8
'''
    功能：获取ip历史记录

'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Base import Base

class IP_history(Base):

    def __init__(self,domain):
        self.domain = domain
        self.ip_history_record = []
        Base.__init__(self)
        self.get_data()


    def get_data(self):
        '''
        功能：从数据库获取原始数据
        '''
        collection = self.mongo_db['domain_dns_rr']
        fetch_data = collection.find({'domain':self.domain},{'_id':False,'domain_ip_cnames':True})
        self.domain_ip_cnames_records = list(fetch_data)[0]['domain_ip_cnames']

    def get_history_record(self):
        '''
        功能：获取ip历史记录(对数据进行整合)
        return:ip_history_record
         [
         {  # 第1次ip记录
           insert_time:---, # 探测时间
            ip_num:--,       # ip数量
            ips:[ip1,ip2, ..., ipn], # ip集合
            reduce_ip:[ip,ip,...], # 减少ip
            add_ip:[ip,ip,,,,]     # 新增ip
        },
        {  # 第2次ip记录
         同上
        }


         ]
        '''
        for item in self.domain_ip_cnames_records:
            cur_record = {}
            cur_record['insert_time'] = item['insert_time']
            cur_record['ip_num'] = len(item['ips'])
            cur_record['ips'] = item['ips']
            cur_record['add_ip'] = item['new']
            cur_record['reduce_ip'] = item['cut']
            self.ip_history_record.append(cur_record)
        return self.ip_history_record



if __name__ == '__main__':
    ip_history_getter = IP_history('00000440.com')
    print ip_history_getter.get_history_record()

# encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..") # 回退到上一级目录
import database.mongo_operation
mongo_conn = database.mongo_operation.MongoConn('10.245.146.37','illegal_domains_profile')
collection_name = 'domain_dns_rr_small'


fetch_data = mongo_conn.mongo_read(collection_name,{'change_times':{'$gt':0}}, {'_id':False},limit_num=None)
string = ''

for item in fetch_data:
    domain = item['domain']
    # 每次的访问记录作为一行
    for visit_record in item['domain_ip_cnames']:
        string = string + str(domain) + '\t' + str(visit_record['insert_time']) + '\t' + str(visit_record['changed'])
        for ip,state in zip(visit_record['ips'],visit_record['ip_state']):
            state_info = 'host:' + str(state['state']) + ';80:' + str(state['state80']) + ';443:' + str(state['state443'])
            string = string + '\t' + ip + '\t' + state_info
        string = string + '\n'



with open('analyze.txt', 'w') as f:
    f.write(string)

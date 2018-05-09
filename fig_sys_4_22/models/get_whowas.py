# encoding:utf-8
"""
获取指定域名的WHOIS和WHOWAS信息，并生成时间线数据结构
"""
from Base import Base


class WhowasData(Base):

    def __init__(self,domain):

        Base.__init__(self)
        self.domain = domain
        self.domain_whois = {}  # 域名WHOIS信息
        self.domain_whowas = []  # 域名WHOWAS数据列表
        self.time_line = []    # 时间线
        self.get_domain_whois()   # 获取域名的whois信息
        self.get_domain_whowas()   # 获取域名的WHOWAS信息

    def get_domain_whois(self):
        """
        获取域名的whois信息
        """
        whois_sql = "SELECT reg_name,reg_email,reg_phone,org_name,insert_time FROM domain_whois WHERE domain = '%s';" %(self.domain) # 获取域名的WHOIS信息
        fetch_data = self.mysql_db.query(whois_sql)
        if fetch_data:
            self.domain_whois = fetch_data[0]
        else:
            self.domain_whois = {}

    def get_domain_whowas(self):
        """
        获取域名的WHOWAS信息
        """
        whowas_sql = "SELECT reg_name,reg_email,reg_phone,org_name,insert_time FROM domain_whowas WHERE domain = '%s';" %(self.domain) # 获取域名的WHOIS信息
        fetch_data = self.mysql_db.query(whowas_sql)
        if fetch_data:
            self.domain_whowas = fetch_data
        else:
            self.domain_whois = []

    def gen_time_line(self):
        """
        根据获取的域名WHOIS和WHOWAS数据，生成timeline格式
        """
        if not self.domain_whois or not self.domain_whowas:   # 如果whois或者WHOWAS为空，则不进行timeline绘制
            return
        self.domain_whois['insert_time'] = self.domain_whois['insert_time'].strftime(
            '%Y-%m-%d %H:%M:%S')  # 将datetime转换为字符串时间
        whois_whowas = self.domain_whowas
        whois_whowas.insert(0,self.domain_whois)

        whois_whowas.sort(key=lambda x: x['insert_time'])   # 升序
        oldest_time = whois_whowas[0]['insert_time']
        for i in range(0, len(whois_whowas)-1):
            old_data = whois_whowas[i]
            new_data = whois_whowas[i+1]
            current_data = self.compare_data(old_data,new_data)
            current_data['time'] = new_data['insert_time']
            self.time_line.append(current_data)

        # 添加最久数据的时间，在前端只显示时间，不显示内容
        self.time_line.append(
            {
                'add': [],
                'reduce': [],
                'change': [],
                'time':oldest_time
             }
        )

    def compare_data(self,old_data,new_data):
        """
        比较两条WHOIS记录各个字段的改变情况
        """
        compare_result = {
            "reduce":[],
            "add": [],
            "change": []
        }
        name_opera = self.compare_field(old_data['reg_name'], new_data['reg_name'], '注册人')
        phone_opera = self.compare_field(old_data['reg_phone'], new_data['reg_phone'], '注册电话')
        email_opera = self.compare_field(old_data['reg_email'], new_data['reg_email'], '注册邮箱')
        org_opera = self.compare_field(old_data['org_name'], new_data['org_name'], '注册公司')

        for opera, field_name, data in (name_opera, phone_opera, email_opera, org_opera):
            if compare_result.has_key(opera):
                compare_result[opera].append([field_name, data[0], data[1]])
        return compare_result

    def compare_field(self, first, second, field_name):
        """
        比较某个字段的两条记录，并记录改变情况，包括same/reduce/add/change四种操作，根据不同操作返回不同数据
        """
        if first == second:  # 两条记录相同
            return 'same', field_name, [first,second]  # 返回任意记录
        elif first and not second:  # 第一条记录有数据，第二条为空
            return 'reduce', field_name, [first,None]  # 返回第一条记录
        elif not first and second:  # 第一条记录无数据，第二条数据有
            return 'add', field_name, [None,second]  # 返回第二条数据
        else:  # 两条都有数据，且不相同
            return ('change', field_name, [first, second])  # 返回两条记录


if __name__ == '__main__':
    domain_sub = WhowasData('3gwz.win')
    domain_sub.gen_time_line()
    print domain_sub.time_line
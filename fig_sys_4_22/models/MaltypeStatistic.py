# -*- coding: utf-8 -*-

from Base import Base

class MalTypeStatistic(Base):
    """
    非法域名类型相关统计类
    """
    def __init__(self):
        Base.__init__(self)

    def count_maltype(self):
        """
        非法域名各类数量统计
        :return: 返回形式 {类型1:数量，类型2：数量,...}
        """
        table_name = "domain_index"

        select_sql = "select maltype,count(*) as num from "+table_name+" group by maltype"
        res = self.mysql_db.query(select_sql)
        results = {}
        for rs in res:
            if rs['maltype'] == "非法赌博".decode('utf8'):
                maltype = 'gamble'
            elif rs['maltype'] == "色情".decode('utf8'):
                maltype = 'porno'
            else:
                maltype = 'other'
            results[maltype]=rs['num']

        return results
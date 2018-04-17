#-*- coding: utf-8 -*-

"""
子域名分析数据
"""

from Base import Base

class QuerySubDomains(Base):
    """
    子域名查询
    """
    def __init__(self):
        Base.__init__(self)

    def get_subdomainsinfo(self,domain):
        """
        获取子域名基本信息
        :return:
        """
        domain_child_table = self.mongo_db.domain_child
        rs = domain_child_table.find_one(
            {'domain':domain},
            {
                '_id':0,
                'ip_s':1,
                'three_level_sub':1,
                'four_level_sub': 1,
                'five_level_sub': 1,
                'six_level_sub': 1,
            }
        )

        if rs is None:
            rs ={
                "sub_sum":0,
                "ip_s":[],
                "three_level_sub":{
                    "dm_set":[],
                    "num":0
                },
                "four_level_sub": {
                    "dm_set": [],
                    "num": 0
                },
                "five_level_sub": {
                    "dm_set": [],
                    "num": 0
                },
                "six_level_sub": {
                    "dm_set": [],
                    "num": 0
                }
            }


        rs['sub_sum'] = rs['three_level_sub']['num']+rs['four_level_sub']['num']+\
                        rs['five_level_sub']['num']+rs['six_level_sub']['num'];

        return rs

if __name__ == "__main__":
    qs = QuerySubDomains()
    # rs =  qs.get_subdomainsinfo('00q165.com')
    rs = qs.get_subdomainsinfo('000033333.com')
    print rs
    print "--------"
    for key,value in rs.iteritems():
        print key,value
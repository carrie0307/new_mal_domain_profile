# -*- coding: utf-8 -*-

import torndb
from pymongo import MongoClient
from copy import copy

class Base(object):

    def __init__(self):
        self.mysql_db = torndb.Connection(
            host = "10.245.146.43",
            database = "mal_domain_profile",
            user = "root",
            password = "platform",
            charset = "utf8",
            time_zone='+8:00'
        )
        # self.mysql_db = torndb.Connection(
        #     host="10.245.146.38",
        #     database="illegal_domains_profile_analysis",
        #     user="root",
        #     password="platform",
        #     charset="utf8",
        #     time_zone='+8:00'
        # )
        self.mongo_db = MongoClient('10.245.146.38',27017).new_mal_domain_profile

    def add_seq_num(self,results,order_by=None):

        if isinstance(results,list):
            res = copy(results)
            if order_by:
                resu = []
                for rs in res:
                    resu.append((rs[order_by],rs))
                resu = sorted(resu, key=lambda x:x[0],reverse=True)
                res = [rs[1] for rs in resu]
                results = res
            for i,rs in enumerate(res):
                results[i]['seq_num']=i+1
        else:
            print "结果非列表形式，添加序列号失败"

        return results

    def None_to_empty(self,result):

        if result is None:
            result = ''

        return result
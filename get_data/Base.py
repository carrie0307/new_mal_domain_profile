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
        )
        self.mongo_db = MongoClient('10.245.146.37',27017).illegal_domains_profile

    def add_seq_num(self,results):

        if isinstance(results,list):
            res = copy(results)
            for i,rs in enumerate(res):
                results[i]['seq_num']=i+1
        else:
            print "结果非列表形式，添加序列号失败"

        return results

    def None_to_empty(self,result):

        if result is None:
            result = ''

        return result

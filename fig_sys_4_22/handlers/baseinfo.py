# encoding:utf-8

"""
基本信息概览handler
"""
import tornado.web
import json
from base_handler import BaseHandler
from models.general_list import QueryDomainGeneralInfo

class DoaminGeneralHandler(BaseHandler):
    """首页控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source =  self.get_argument('source','general')
        maltype = source if source!='general' else(None)
        if maltype== "gamble":
            maltype = "非法赌博"
        elif  maltype== "porno":
            maltype = "色情"
        else:
            maltype = None
        data = QueryDomainGeneralInfo().get_general_list(maltype=maltype)
        self.render(
            'domain_general.html',
            source = json.dumps(source),
            data=json.dumps(data)
        )
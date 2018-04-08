# encoding:utf-8

"""
非法域名关键信息查询handler
"""
import tornado.web
import json
from models.general_list import QueryDomainGeneralInfo
from base_handler import BaseHandler

class KeyinfoQueryHandler(BaseHandler):
    """非法域名关键信息查询控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source = self.get_argument('source', 'sponsoring_registrar')
        value = self.get_argument('value', '1API GmbH')
        data1 = QueryDomainGeneralInfo().get_general_list(source=source,source_value=value,maltype="非法赌博")
        data2 = QueryDomainGeneralInfo().get_general_list(source=source, source_value=value, maltype="色情")
        self.render(
            'keyinfo_query.html',
            data = json.dumps([data1,data2]),
            source = json.dumps(source),
            value = json.dumps(value)
        )

class KeyinfoDataHandler(BaseHandler):
    """非法域名关键信息查询控制"""

    @tornado.web.authenticated
    def get(self):

        self.get_authenticated()
        source = self.get_argument('source', '')
        value = self.get_argument('value', '')
        data1 = QueryDomainGeneralInfo().get_general_list(source=source,source_value=value,maltype="非法赌博")
        data2 = QueryDomainGeneralInfo().get_general_list(source=source, source_value=value, maltype="色情")
        data = json.dumps([data1,data2])
        self.write(data)
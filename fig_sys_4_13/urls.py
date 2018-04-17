#coding=utf-8
"""
系统路由设置
"""

# 登陆控制
from handlers.login import LoginHandler
# 首页控制
from handlers.index import IndexHandler,RelativeORGHandler
# 非法域名关键信息查询控制
from handlers.keyinfo_query import KeyinfoQueryHandler
from handlers.keyinfo_query import KeyinfoDataHandler
# 非法域名全国地理位置归属统计控制
from handlers.pos_statistics import PosStatisticsHandler
from handlers.pos_statistics import PosStatisticsDataHandler
from handlers.pos_statistics import PosStaMapDataHandler
#非法域名关键信息总表预览控制
from handlers.key_statistic import KeyStatisticsGeneralHandler
from handlers.key_statistic import KeyStatisticsViewHandler
from handlers.key_statistic import KeyStatisticsViewDataHandler
#基本信息概览
from handlers.baseinfo import DoaminGeneralHandler
#域名画像查询
from handlers.domain_figure import DomainFigureHandler
from handlers.domain_figure import ICPAnalyseDataHandler,IPAnalyseDataHandler,WHOISAnalyseDataHandler,SubDomainDataHandler
from handlers.domain_figure import PosAnalyseDataHandler,LinksAnalyseDataHandler,ContentAnalyseDataHandler,ALLAnalyseDataHandler
#团伙分析
from handlers.IllegalOrgsHandler import IllegalOrgsHandler
#关联关系控制
from handlers.relative_relation import VisualHandler,GroupHandler

#内外链总览控制
from handlers.link_total import LinksTotalHandler
#IP历史状态探测控制
from handlers.domain_status_history import IPHistoryHandler, IPHistoryDataHandler, WhoisHistoryHandler, ContentHistoryHandler

urls = [
    # 登陆控制
    (r'/login', LoginHandler),
    # 首页控制
    (r'/', IndexHandler),
    #关联关系控制
    (r'/visual',VisualHandler),
    (r'/group',GroupHandler),
    #相关机构控制
    (r'/relative_org', RelativeORGHandler),
    #基本信息概览
    (r'/baseinfo', DoaminGeneralHandler),
    # (r'/baseinfo/data', DoaminGeneralDataHandler),
    #团伙分析查询控制
    (r'/illegal_orgs_query', IllegalOrgsHandler),
    # 非法域名关键信息查询控制
    (r'/keyinfo_query', KeyinfoQueryHandler),
    (r'/keyinfo_query/data', KeyinfoDataHandler),
    #域名画像查询控制
    (r'/domain_figure_query', DomainFigureHandler),
    (r'/icp_analyse/data', ICPAnalyseDataHandler),
    (r'/ip_analyse/data', IPAnalyseDataHandler),
    (r'/whois_analyse/data', WHOISAnalyseDataHandler),
    (r'/pos_analyse/data', PosAnalyseDataHandler),
    (r'/links_analyse/data', LinksAnalyseDataHandler),
    (r'/content_analyse/data', ContentAnalyseDataHandler),
    (r'/sub_domain/data', SubDomainDataHandler),
    (r'/all_analyse/data', ALLAnalyseDataHandler),
    # 非法域名关键信息总表预览控制
    (r'/keyinfo_general_list', KeyStatisticsGeneralHandler),#总览
    (r'/keyinfo_overview_list', KeyStatisticsViewHandler),#概览
    (r'/keyinfo_overview_list/data', KeyStatisticsViewDataHandler),
    # 非法域名全国地理位置归属统计控制
    (r'/pos_statistics', PosStatisticsHandler),
    (r'/pos_statistics/pos_data', PosStatisticsDataHandler),
    (r'/pos_statistics/map_data', PosStaMapDataHandler),

    #内外链总览控制
    (r'/links_total', LinksTotalHandler),
    #IP历史状态探测控制
    (r'/ip_history', IPHistoryHandler),
    (r'/ip_history/data', IPHistoryDataHandler),
    (r'/whois_history', WhoisHistoryHandler),
    (r'/content_history', ContentHistoryHandler),
]
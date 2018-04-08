# -*- coding: utf-8 -*-

from Base import Base

class QueryWebResults(Base):
    """
    页面结果查询
    """
    def __init__(self):
        Base.__init__(self)

    def convert_shape(self,res):
        """
        转换结果形式
        :param res: 查询结果
        :return: {
            title:页面标题,
            keywords:页面关键词,
            description:页面描述,
            redirect_domain:重定向域名,
            shot_path:页面快照路径,
            detect_time:检测时间,
            flag:页面是否成功获取
            }
        """
        res = dict(res)
        result = dict(
            title=self.None_to_empty(res.get('top_title')),
            meta =self.None_to_empty(res.get('meta')),
            redirect_domain=self.None_to_empty(res.get('current_url')),
            shot_path=self.None_to_empty(res.get('shot_path')),
            detect_time=str(self.None_to_empty(res.get('cur_time')))
        )
        flag = 0
        for value in result.values():
            if value != '':
                flag = 1
                break
        result['flag'] = flag  # flag=0表示域名已不存在或页面访问失败

        return result

    def get_web_baseinfo(self,domain,query_all=False):
        """
        获取页面内容信息(内容分析)
        :param domain: 待查域名
        :param query_all: 是否获取历史记录
        :return: 最新记录row形式:{
            title:页面标题,
            keywords:页面关键词,
            description:页面描述,
            redirect_domain:重定向域名,
            shot_path:页面快照路径,
            detect_time:检测时间,
            flag:页面是否成功获取
            }
            历史记录:[row,row,row,...,row]#由最新探测记录,...,首次探测记录
        """
        domain_web_table = self.mongo_db.domain_web
        if query_all:
            res = domain_web_table.find_one(
                {'domain': domain},
                {
                    'content': 1,
                    '_id':0
                }
            )
            content = res['content']
            results = []
            if len(content)!=0:
                for elem in reversed(content):
                    results.append(self.convert_shape(elem))

            return results
        else:
            res = domain_web_table.find_one(
                {'domain': domain},
                {
                    'row': {
                        '$slice': -1
                    },
                    '_id':0
                }
            )
            if res.get('row'):
                res = res['row'][0]
            else:
                res = {'shot_path':'shot_files/error.png'}
            result = self.convert_shape(res)

            return result

    def get_links_baseinfo(self, domain):

        links_relation = self.mongo_db.links_relation
        result = links_relation.find_one(
            {'domain':domain},
            {
                'links_outer':1,
                'links_enter':1,
                '_id':0
            }
        )
        links_enter_num = result['links_enter']['num']
        links_outer_num = result['links_outer']['num']
        illegal_links_enter_num = result['links_enter']['illegal_links_enter']['num']
        legal_links_enter_num = result['links_enter']['legal_links_enter']['num']
        inter_links_num =result['links_outer']['inter_links']['num']
        outer_links_num =result['links_outer']['outer_links']['num']
        hidden_links_num =result['links_outer']['hidden_links']['num']
        enter_domains = set()
        enter_urls = result['links_enter']['legal_links_enter']['links']\
                     +result['links_enter']['illegal_links_enter']['links']
        for rs in enter_urls:
            enter_domains.add(rs['domain'])
        enter_domains_num = len(enter_domains)
        outer_domains = set()
        outer_urls = result['links_outer']['outer_links']['links']
        for rs in outer_urls:
            outer_domains.add(rs['domain'])
        outer_domains_num = len(outer_domains)
        result = {
            'num':[
                links_enter_num,
                links_outer_num,
                illegal_links_enter_num,
                legal_links_enter_num,
                inter_links_num,
                outer_links_num,
                hidden_links_num
            ],
            'rate':[]
        }
        if enter_domains_num==0:
            result['rate'].append(0)#分母为0
        else:
            result['rate'].append(links_enter_num/enter_domains_num)
        if outer_links_num == 0:
            result['rate'].append(0)#"分母为0"
        else:
            result['rate'].append(outer_links_num / outer_domains_num)
        if outer_links_num == 0:
            result['rate'].append(0)#"分母为0"
        else:
            result['rate'].append((links_outer_num+ links_outer_num)/ outer_links_num)

        return result

    def get_links_info(self,domain):
        """
        获取页面链接信息（内外链分析）
        :param domain: 待查询域名
        :return: {
            links_outer(链出信息)：{
                num : 链出数量,
                hidden_links(暗链信息):{
                    links:暗链链接[{url:链接,domain:域名},...],
                    num:暗链链接数量
                },
                outer_links(外链链信息):{
                    links:外链链接[{url:链接,domain:域名},...],
                    num:外链链接数量
                },
                inter_links(暗链信息):{
                    links:内链链接[{url:链接,domain:域名},...],
                    num:内链链接数量
                }
            },
            links_enter(链入信息)：{
                num : 链入数量,
                legal_links_enter(合法链入信息):{
                    links:合法链入链接[{url:链接,domain:域名},...],
                    num:合法链入链接数量
                    },
                illegal_links_enter(非法链入信息):{
                    links:非法链入链接[{url:链接,domain:域名},...],
                    num:非法链入链接数量
                    }
            },
            rate(比例信息):[链入url/链入domain,外链url/外链domain,所有url/外链url]
        }
        """
        links_relation = self.mongo_db.links_relation
        result = links_relation.find_one(
            {'domain':domain},
            {
                'links_outer':1,
                'links_enter':1,
                '_id':0
            }
        )
        result['rate'] = []
        outer_urls = result['links_outer']['outer_links']['links']
        outer_urls_num = result['links_outer']['outer_links']['num']*1.0
        outer_domains = set()
        for rs in outer_urls:
            outer_domains.add(rs['domain'])
        outer_domains_num = len(outer_domains)
        enter_urls = result['links_enter']['legal_links_enter']['links']\
                     +result['links_enter']['illegal_links_enter']['links']
        enter_urls_num = result['links_enter']['num']*1.0
        enter_domains = set()
        for rs in enter_urls:
            enter_domains.add(rs['domain'])
        enter_domains_num = len(enter_domains)
        all_num = result['links_enter']['num']+result['links_outer']['num']*1.0

        if enter_domains_num==0:
            result['rate'].append("分母为0")
        else:
            result['rate'].append("%.2f%%" % (enter_urls_num/enter_domains_num*100))
        if outer_domains_num == 0:
            result['rate'].append("分母为0")
        else:
            result['rate'].append("%.2f%%" % (outer_urls_num / outer_domains_num * 100))
        if enter_domains_num == 0:
            result['rate'].append("分母为0")
        else:
            result['rate'].append("%.2f%%" % (all_num / outer_urls_num * 100))

        return result

if __name__ == "__main__":
    qw = QueryWebResults()
    print qw.get_web_baseinfo('277488.com',query_all=False)
    # print qw.get_web_baseinfo('277488.com',query_all=True)
    # print qw.get_links_baseinfo('000000.com')
    # content_analyse_results = QueryWebResults().get_web_baseinfo('000000.com', query_all=False)
    # if content_analyse_results['shot_path'] is not None and content_analyse_results['shot_path'] != '':
    #     shot_result = "获取成功"
    # else:
    #     shot_result = "获取失败"
    # if content_analyse_results['redirect_domain'] is not None and content_analyse_results['redirect_domain'] != '':
    #     analyse_results = [
    #         ["页面标题", content_analyse_results['title']],
    #         ["页面关键词", content_analyse_results['keywords']],
    #         ["重定向域名", content_analyse_results['redirect_domain']],
    #         ["页面描述", content_analyse_results['description']],
    #         ["快照获取", shot_result],
    #         ["探测时间", content_analyse_results['detect_time']],
    #     ]
    # else:
    #     analyse_results = [
    #         ["页面标题", content_analyse_results['title']],
    #         ["页面关键词", content_analyse_results['keywords']],
    #         ["页面描述", content_analyse_results['description']],
    #         ["快照获取", shot_result],
    #         ["探测时间", content_analyse_results['detect_time']],
    #     ]
    # shot_path = content_analyse_results['shot_path']
    # print analyse_results
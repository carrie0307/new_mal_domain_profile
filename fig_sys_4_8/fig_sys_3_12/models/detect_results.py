# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from Base import Base

class QueryDetectResut(Base):
    """
    第三方接口检测域名恶意性结果查询类
    """

    def __init__(self):
        Base.__init__(self)

    @staticmethod
    def extract_maltype(single_result,default_type):
        """
        提取安全类别，组合成字典形式：{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间}
        :param single_result: {_rs:检测结果,_it:检测时间}
        :param default_type: 检测工具
        :return: {detect_result:检测结果,detect_type:安全级别,detect_time:检测时间}
        """
        if default_type == 'tencent':
            single_result['detect_time'] = str(single_result['tm_it'])
            del single_result['tm_it']
            result = single_result.get('tm_rs')
            single_result['detect_result'] = result
            del single_result['tm_rs']
            if result.find('危险')!=-1:
                single_result['detect_type'] = "危险"
            elif result.find('未知')!=-1:
                single_result['detect_type'] = "未知"
            elif result.find('安全')!=-1:
                single_result['detect_type'] = "安全"
            else:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
                print "新类型，重新区分/还未检测"

        elif default_type == 'baidu':
            single_result['detect_time'] = str(single_result['bd_it'])
            del single_result['bd_it']
            result = single_result.get('bd_rs')
            del single_result['bd_rs']
            single_result['detect_result'] = result
            if result is None:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
            else:
                single_result['detect_type'] = result
        elif default_type == 'sanliuling':
            single_result['detect_time'] = str(single_result['sl_it'])
            del single_result['sl_it']
            result = single_result.get('sl_rs')
            del single_result['sl_rs']
            single_result['detect_result'] = result
            if result is None:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
            elif result in ["高危",'严重','警告']:
                single_result['detect_type'] = "危险"
            elif result=='安全':
                single_result['detect_type'] = "安全"
            elif result.find('未知')!=-1:
                single_result['detect_type'] = "未知"
                single_result['detect_result'] = "安全性得分未知"
            else:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
                print "新类型，重新区分/还未检测"
        elif default_type == 'jinshan':
            single_result['detect_time'] = str(single_result['js_it'])
            del single_result['js_it']
            result = single_result.get('js_rs')
            del single_result['js_rs']
            single_result['detect_result'] = result
            if result is not None and result in ["危险","安全","未知"]:
                single_result['detect_type'] = result
            else:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
        elif default_type == 'macfree':
            single_result['detect_time'] = str(single_result['mf_it'])
            del single_result['mf_it']
            result = single_result.get('mf_rs')
            del single_result['mf_rs']
            if result == "High Risk":
                single_result['detect_result']="高度风险"
                single_result['detect_type'] = "危险"
            elif result == "Medium Risk":
                single_result['detect_result'] = "中度风险"
                single_result['detect_type'] = "危险"
            elif result == "Minimal Risk":
                single_result['detect_result'] = "低度风险"
                single_result['detect_type'] = "安全"
            elif result == "Univerified":
                single_result['detect_result'] = "风险未知"
                single_result['detect_type'] = "未知"
            else:
                single_result['detect_type'] = "待检测"
                single_result['detect_result'] = "检测结果未知"
        elif default_type == 'virustotal':
            single_result['detect_time'] = str(single_result['vt_it'])
            del single_result['vt_it']
            result = single_result.get('vt_rs')
            del single_result['vt_rs']
            if result is None:
                single_result['detect_result'] = "检测结果未知"
                single_result['detect_type'] = "待检测"
            else:
                result = eval(result)
                single_result['detect_result'] = str(result['malicious rate'])
                if str(result['malicious rate'])[0]!="0":
                    single_result['detect_type'] = "危险"
                elif str(result['unrated_rate'])[0]!="0":
                    single_result['detect_type'] = "未知"
                else:
                    single_result['detect_type'] = "安全"
        else:
            single_result = dict(
                detect_result = '',
                detect_type = '',
                detect_time = ''
            )
            print "输入类型错误..."

        return single_result

    @staticmethod
    def convert_shape(result,default_type):
        """
        组合成字典形式
        :param result: {_rs:检测结果,_it:检测时间}
        :param default_type: all/tencent/baidu/sanliuling/jinshan/macfree/virustotal
        :return: all对应的结果为{
                'tencent':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间},
                'baidu':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间},
                ...
                'virustotal':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间}
        }
        """
        if not isinstance(result,dict):
            print "非字典形式，无法转换"
            return result
        else:
            if default_type != 'all':
                converted_result = QueryDetectResut.extract_maltype(result,default_type)
            else:
                tm_result = QueryDetectResut.extract_maltype(dict(
                    tm_rs =result['tm_rs'],
                    tm_it=result['tm_it']
                ),'tencent')
                bd_result = QueryDetectResut.extract_maltype(dict(
                    bd_rs =result['bd_rs'],
                    bd_it=result['bd_it']
                ),'baidu')
                sl_result = QueryDetectResut.extract_maltype(dict(
                    sl_rs =result['sl_rs'],
                    sl_it=result['sl_it']
                ),'sanliuling')
                js_result = QueryDetectResut.extract_maltype(dict(
                    js_rs =result['js_rs'],
                    js_it=result['js_it']
                ),'jinshan')
                mf_result = QueryDetectResut.extract_maltype(dict(
                    mf_rs =result['mf_rs'],
                    mf_it=result['mf_it']
                ),'macfree')
                vt_result = QueryDetectResut.extract_maltype(dict(
                    vt_rs =result['vt_rs'],
                    vt_it=result['vt_it']
                ),'virustotal')
                converted_result = {
                    'tencent':tm_result,
                    'baidu':bd_result,
                    'sanliuling':sl_result,
                    'jinshan':js_result,
                    'macfree':mf_result,
                    'virustotal':vt_result
                }
            return converted_result

    def get_detect_results(self,domain,default_type='all'):
        """
        获取对应工具的检测结果字典{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间}
        :param domain: 待检测域名
        :param default_type: 默认值为all，可选择tencent/baidu/sanliuling/jinshan/macfree/virustotal
        :return: 默认情况下的结果{
                'tencent':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间},
                'baidu':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间},
                ...
                'virustotal':{detect_result:检测结果,detect_type:安全级别,detect_time:检测时间}
                }
        """
        if default_type == 'tencent':
            sql = "select TencentManager_result as tm_rs,tm_insert_time as tm_it " \
                  " from detect_results where domain=%s"
        elif default_type == 'baidu':
            sql = "select BaiduDefender_result as bd_rs,bd_insert_time as bd_it " \
                  " from detect_results where domain=%s"
        elif default_type == 'sanliuling':
            sql = "select sanliuling_result as sl_rs,sl_insert_time as sl_it " \
                  " from detect_results where domain=%s"
        elif default_type == 'jinshan':
            sql = "select jinshan_result as js_rs,js_insert_time as js_it " \
                  " from detect_results where domain=%s"
        elif default_type == 'macfree':
            sql = "select macfree_result as mf_rs,mf_insert_time as mf_it " \
                  " from detect_results where domain=%s"
        elif default_type == 'virustotal':
            sql = "select virustotal_result as vt_rs,vt_insert_time as vt_it " \
                  " from detect_results where domain=%s"
        else:#default
            sql = "select TencentManager_result as tm_rs,tm_insert_time as tm_it," \
                  "BaiduDefender_result as bd_rs,bd_insert_time as bd_it," \
                  "sanliuling_result as sl_rs,sl_insert_time as sl_it," \
                  "jinshan_result as js_rs,js_insert_time as js_it," \
                  "macfree_result as mf_rs,mf_insert_time as mf_it," \
                  "virustotal_result as vt_rs,vt_insert_time as vt_it " \
                  " from detect_results where domain=%s"

        result = self.mysql_db.get(sql,domain)

        converted_result = QueryDetectResut.convert_shape(result,default_type)

        return converted_result

if __name__ == "__main__":
    qr = QueryDetectResut()
    # print qr.get_detect_results('0-360c.com','tencent')
    # print qr.get_detect_results('0-360c.com', 'baidu')
    # print qr.get_detect_results('0-360c.com', 'sanliuling')
    # print qr.get_detect_results('0-360c.com', 'jinshan')
    # print qr.get_detect_results('0-360c.com', 'macfree')
    # print qr.get_detect_results('0-360c.com', 'virustotal')
    res = qr.get_detect_results('000000.in')
    for key,value in res.iteritems():
        print key
        for k,v in value.iteritems():
            print k
            print v
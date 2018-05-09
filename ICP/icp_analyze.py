# encoding:utf-8
"""
    icp分析:包括 page_icp的查重和icp比对结果（注意运行时更新选择条件的flag位）

    author：csy
"""
import re
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..") # 回退到上一级目录
import database.mysql_operation

'''数据库连接'''
mysql_conn = database.mysql_operation.MysqlConn('10.245.146.37','root','platform','illegal_domains_profile','utf8')

def page_recheck(flag):
    """
    page_icp查重分析
    """

    sql = "SELECT page_icp,count(*) FROM domain_icp WHERE flag = %d AND page_icp != '-1' AND page_icp != '--' GROUP BY page_icp;" %(flag)
    fetch_data = mysql_conn.exec_readsql(sql)
    for page_icp,count in fetch_data:
        if page_icp == '--' or page_icp == '-1':
            continue
        if count < 2:
            continue
        sql = "SELECT domain FROM domain_icp WHERE page_icp = '%s';" %(page_icp)
        fetch_data = mysql_conn.exec_readsql(sql)
        domains = [item[0] for item in fetch_data]
        reuse_domains = ';'.join(domains)
        sql = "UPDATE domain_icp SET reuse_check = '%s' WHERE page_icp = '%s';" %(reuse_domains,page_icp)
        print reuse_domains,page_icp
        exec_res = mysql_conn.exec_cudsql(sql)
    sql = "UPDATE domain_icp SET reuse_check = '未获取到页面ICP' WHERE page_icp ='-1' or page_icp = '--';"
    exec_res = mysql_conn.exec_cudsql(sql)
    sql = "UPDATE domain_icp SET reuse_check = '未发现重复' WHERE reuse_check is NULL;"
    exec_res = mysql_conn.exec_cudsql(sql)
    mysql_conn.commit()


def icp_cmp(flag):
    """
    icp比对
    """

    sql = "SELECT domain,auth_icp,page_icp FROM domain_icp WHERE flag = %d;" %(flag)
    fetch_data = mysql_conn.exec_readsql(sql)
    for item in fetch_data:
        domain,auth_icp,page_icp = item
        print domain,auth_icp,page_icp
        icp_cmp_res = get_icp_cmp_res(auth_icp,page_icp)
        print domain,icp_cmp_res
        sql = "UPDATE domain_icp SET icp_tag = '%s' WHERE domain = '%s'" %(icp_cmp_res,domain)
        exec_res = mysql_conn.exec_cudsql(sql)
    mysql_conn.commit()
    print '特征分析完成...'


def std_deal_icp(icp):
    '''
    功能： 对icp进行标准化处理，只比对主体的号码
    '''

    if icp == '-1' or icp == '--':
        return icp
    if not isinstance(icp,unicode):
        encode = chardet.detect(icp)['encoding']
        icp = unicode(icp, encode)
    if 'ICP' in icp:
        # 说明提取到的是ICP，不是增值营业号码
        # 只提取ICP的主体部分  青ICP证：09000092号 -- 青09000092
        pattern = re.compile(u'([\u4e00-\u9fa5]{0,1})ICP[\u4e00-\u9fa5]{0,1}.*?([\d]{6,8})[\u53f7]*-*[\d]*').findall(icp)
        if pattern:
            print pattern
            icp = (pattern[0][0] + pattern[0][1]).strip()
    elif 'B2' in icp:
        # QUESTION: 无法匹配到B2前的汉字浙B2-20110001-7
        # 浙B2-20110001-7  - B2-20110001-7 / B2-20110001-7   - B2-20110001
        pattern = re.compile(u'([\u4e00-\u9fa5]{0,1}[A-B][1-2]-[\d]{6,8})-*?[\d]*').findall(icp)
        if pattern:
            icp = pattern[0]
    return icp


def get_icp_cmp_res(auth_icp,page_icp):
    """
    icp比对：(icp_cmp()调用)
    auth_icp 的两类取值：icp，--
    page_icp 的三类去值：icp，-1,--

    icp 比对：
    1. page 无法访问   -- 页面ICP无法获取
    2. auth_icp无，page_icp无  -- 无ICP
    3. auth_icp有，page_icp无 -- 页面未显示ICP
    4. auth_icp有，page_icp有，且相同 -- ICP信息正常
    5. 其他： 虚假ICP(auth_icp无，page_icp有,auth_icp有，page_icp有，且不同)
    """
    auth_icp = std_deal_icp(auth_icp)
    page_icp = std_deal_icp(page_icp)

    if page_icp == '-1':
        return '页面ICP无法获取'
    elif auth_icp == '--' and page_icp == '--':
        return '无ICP'
    elif auth_icp != '--' and page_icp == '--':
        return '页面未显示ICP'
    elif auth_icp != '--' and page_icp != '--' and auth_icp == page_icp:
        return 'ICP正常'
    else:
        return '虚假ICP'


def main():
    flag = 1
    # page_recheck(flag)
    # print '查重处理完成...'
    icp_cmp(flag)
    print '特征分析完成...'





if __name__ == '__main__':
    main()
    # 粤ICP备11086197号-1	粤ICP备11086197号
    # 苏ICP备06057086号-1	苏ICP备06057086号
    # 浙B2-20110001-7	B2-20110001
    # 浙B2-20110489-3
    # print get_icp_cmp_res('浙B2-20110001-7','B2-20110001')
    # s = '浙ICP备-20150105号-3'
    # print chardet.detect(s)['encoding']
    # s = '浙B2-20140102-9'
    # print chardet.detect(s)['encoding']
    # print std_deal_icp('粤ICP备11086197号')
    # print std_deal_icp('浙B2-20110001-7')

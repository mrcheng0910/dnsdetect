#!/usr/bin/python
#encoding:utf-8

import urllib2
import json
import MySQLdb
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from gevent import monkey
monkey.patch_all()
import gevent

THREAD_NUM = 10

def get_con():

    host = 'localhost'
    user = 'root'
    passwd = 'cynztt'
    db  = 'dns_detect'
    charset = 'utf8'
    try:
        conn = MySQLdb.Connection(host = host,user = user,passwd=passwd,db =db,charset = charset)
    except MySQLdb.Error,e:
        print "Mysql error %d: %s" %(e.args[0],e.args[1])
        sys.exit(1)
    return conn


def get_ip():

    conn = get_con()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT  ip FROM dns_ip where (country = '' or country is null)" ) #获得要查询的ip
        ips = cursor.fetchall()
    except:
        print "Select Failed"
        conn.rollback()
        sys.exit(1)
    
    return ips

def check_ip(ip):
    sql = "update dns_ip set country = %s,region = %s,city = %s,isp = %s  where ip = %s "
    apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip[0]

    try:
        content = urllib2.urlopen(apiurl,timeout = 5).read()
    except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
        print "The server couldn't fulfill the request"
        # print "Error code:",e.code
        # print "Return content:",e.read()
        return

    except urllib2.URLError,e:    #无法得到service
        print "Failed to reach the server"
        # print "The reason:",e.reason
        return
    except socket.timeout as e:
        print 'timeout'
        return

    else:

        data = json.loads(content)['data']
        code = json.loads(content)['code']
        if code ==0:
            str_print = "IP: %s  From: %s%s%s  ISP: %s" % (data['ip'], data['country'], data['region'], data['city'], data['isp'])
            print str_print
            try:
                cursor.execute(sql,(data['country'],data['region'],data['city'],data['isp'],ip[0]))    
            except:
                print "Update failed" 
                conn.rollback()  #发生错误时候回滚
                return           
        else:
            print data
            return
    conn.commit()
    
def main():

    ip_list = []
    ip_list = get_ip()
    rowcount = len(ip_list)
    count = 0
    while count * THREAD_NUM < rowcount:
        ips = ip_list[count * THREAD_NUM: (count + 1) * THREAD_NUM]
        gevent.joinall([gevent.spawn(check_ip, ip) for ip in ips])
        # gevent.joinall([
        #     gevent.spawn(check_ip,ips[0][0] ),
        #     gevent.spawn(check_ip,ips[1][0] ),
        #     gevent.spawn(check_ip,ips[3][0] ),
        #     gevent.spawn(check_ip,ips[2][0] ),
        #     gevent.spawn(check_ip,ips[4][0] ),
        #     ])
        ips = []
        count = count + 1

    cursor.close()
    conn.close()
    print 'done'

if __name__ == '__main__':
    main()

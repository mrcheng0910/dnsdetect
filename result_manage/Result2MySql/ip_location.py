#!C:\Python27\python
#encoding:utf-8
import urllib2
import json
import MySQLdb
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf8')

UPDATE_RATE = 50


conn=MySQLdb.Connection(host='localhost',user='root',passwd='cynztt',db='dns_detect',charset='utf8')
cursor = conn.cursor()


def get_ip():
    try:
        cursor.execute("SELECT  ip FROM dns_ip where (country = '' or country is null)" ) #获得要查询的ip
        ips = cursor.fetchall()
    except:
        print "select failed"
        conn.rollback()
        sys.exit(1)

    return ips

def check_ip(ips):
    sql = "update dns_ip set country = %s,region = %s,city = %s,isp = %s  where ip = %s "
    i = 0
    for ip in ips:
        apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % str(ip[0]).strip()

        try:
     
            content = urllib2.urlopen(apiurl,timeout = 10).read()
        
        except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
            print "The server couldn't fulfill the request"
            print "Error code:",e.code
            print "Return content:",e.read()
            continue

        except urllib2.URLError,e:    #无法得到service
            print "Failed to reach the server"
            print "The reason:",e.reason
            continue
        except socket.timeout as e:
            print 'timeout'
            continue

        else:

            data = json.loads(content)['data']
            code = json.loads(content)['code']
            if code ==0:
                str_print = "IP: %s  From: %s%s%s  ISP: %s" % (data['ip'], data['country'], data['region'], data['city'], data['isp'])
                print str_print
                try:
                    cursor.execute(sql,(data['country'],data['region'],data['city'],data['isp'],ip[0]))
                    i = i + 1
                    if i == UPDATE_RATE:
                        conn.commit()
                        i = 0
                except:
                    print "Update failed" 
                    conn.rollback()  #发生错误时候回滚
                    continue            
            else:
                print data

    conn.commit()
    cursor.close()
    conn.close()
    print 'done'

def main():

    ips = []
    ips = get_ip()
    check_ip(ips)

if __name__ == '__main__':
    main()

#encoding:utf-8  
"""
优化代码，功能合理分类
"""
import sys
import socket
import random
import select
from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode
import operator
import MySQLdb
import time
from gevent import monkey; monkey.patch_all()
import gevent

THREAD_NUM = 20 #进程数量

 # current_time = time.strftime("%Y-%m-%d %X",time.localtime())
current_time = time.strftime("%Y-%m-%d",time.localtime())

def check_ip(ip):
    """
    验证可以对外提供服务的DNS的ip，并将结果存入数据库
    """

    DPORT = 53                      #默认端口是53
    tid = random.randint(0,65535)   #tid为随机数
    opcode = Opcode.QUERY           #标准查询
    qtype = Type.A                  #查询类型为A
    qclass = Class.IN               #查询类IN
    rd = 1                          #期望递归查询

    domain_list = ['www.baidu.com','www.sina.com','www.163.com','www.ifeng.com','www.hitwh.edu.cn'] # 要查询的域名

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             #建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    except socket.error,msg:
        print "无法创建socket.Error code:" +str(msg[0])+',Error message:'+msg[1]    #error
        sys.exit(1)
    source_port = random.randint(1024, 65535) #windows不是65535                #随机port
    s.bind(('', source_port))  #绑定，检测所有接口

    result = []             #得到的结果
    result_ip = []
    result_diffrences = []
    ip_source = []
        
    for domain in domain_list:
     
        try:
            m = Lib.Mpacker()
            m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
            m.addQuestion(domain,qtype,qclass)
            request = m.getbuf()
        except:
            print 'test'
            pass

        try:
            s.sendto(request,(ip, DPORT))
            print 'domain: ',domain," send to Dns server:",ip
        except socket.error,reason:
            print  reason
            continue
                                      
        '''循环接收收到的返回header'''
    while 1:
        try:
            r,w,e = select.select([s], [], [],3)
            if not (r or w or e):
                break
            (data,addr) = s.recvfrom(65535)
            u = Lib.Munpacker(data)
            r = Lib.DnsResult(u,{})

            if r.header['status'] == 'NOERROR' and len(r.answers): #判断可解析条件

                result.append({'domain' : r.questions[0]['qname'],'ip' : addr[0] ,'domain_info':'yes'})
                print r.questions[0]['qname'] + '\t' + addr[0] + ' success'
                break
            else:
                if len(r.questions) != 0:
                    result.append({'domain' : r.questions[0]['qname'],'ip' : addr[0],'domain_info':'failed'})
                    print r.questions[0]['qname'] + '\t' + addr[0] + ' failed'
                    break
                else:
                    result.append({'domain' : r.questions[0]['qname'],'ip' : addr[0],'domain_info':'other'})
                    print 'questions is wrong'
        except socket.error, reason:
            print reason
            continue

        except:
            continue

    result2sql(result)


def result2sql(results):
    """
    结果存入数据库
    """
    if not results:
        return
    try:
        cursor.execute('UPDATE test SET find_num = (find_num + 1),snoop_cyn = %s  WHERE dns_ip = %s and date = %s ',('1',results[0]['ip'],current_time))
        conn.commit()
    except:
        print 'Update failed'
        conn.rollback()

def main():
    """
    测试函数
    """

    fr = open('ip_source.txt',"r")
    ip_list = fr.readlines()
    rowcount = len(ip_list)
    count = 0
    sql = 'INSERT IGNORE INTO test(dns_ip,date) VALUES (%s,%s)'
    for ip in ip_list:
        cursor.execute(sql,(ip.strip(),current_time))
    conn.commit()


    while count * THREAD_NUM < rowcount:
        ips = ip_list[count * THREAD_NUM : (count + 1) * THREAD_NUM]
        gevent.joinall([ gevent.spawn(check_ip,ip.strip()) for ip in ips ])
        # gevent.joinall([
        #     gevent.spawn(check_ip,ips[0][0] ),
        #     gevent.spawn(check_ip,ips[1][0] ),
        #     gevent.spawn(check_ip,ips[3][0] ),
        #     gevent.spawn(check_ip,ips[2][0] ),
        #     gevent.spawn(check_ip,ips[4][0] ),
        #     ])
        ips = []
        count = count + 1
    
    fr.close()

if __name__ == "__main__":

    main()

    cursor.execute('UPDATE test SET num = (num + 1)  WHERE date = %s ',(current_time))
    conn.commit()
    cursor.close()
    conn.close()

# encoding:utf-8
"""
优化代码，功能合理分类
"""
import sys
sys.path.append('..')
import socket
import random
import select
from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode
# import operator
import time
from gevent import monkey
monkey.patch_all()
import gevent

THREAD_NUM = 30  # 进程数量

# current_time = time.strftime("%Y-%m-%d %X",time.localtime())
current_time = time.strftime("%Y-%m-%d", time.localtime())


def check_ip(ip):
    """
    验证可以对外提供服务的DNS的ip，并将结果存入数据库
    """
    print ip
    DPORT = 53  # 默认端口是53
    tid = random.randint(0, 65535)  # tid为随机数
    opcode = Opcode.QUERY  # 标准查询
    qtype = Type.A  # 查询类型为A
    qclass = Class.IN  # 查询类IN
    rd = 1  # 期望递归查询

    # domain_list = ['www.baidu.com', 'www.sina.com',
    # 'www.163.com', 'www.ifeng.com', 'www.hitwh.edu.cn']  # 要查询的域名
    domain_list = ['www.zxcs188.com']

    try:
        # 建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        # error
        print "无法创建socket.Error code:" + str(msg[0]) + ',Error message:' + msg[1]
        sys.exit(1)
    # windows不是65535                #随机port
    source_port = random.randint(1024, 65535)
    s.bind(('', source_port))  # 绑定，检测所有接口

    result = []  # 得到的结果
    result_ip = []
    result_diffrences = []
    ip_source = []

    for domain in domain_list:

        try:
            m = Lib.Mpacker()
            m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
            m.addQuestion(domain, qtype, qclass)
            request = m.getbuf()
        except:
            print 'test'
            pass

        try:
            s.sendto(request, (ip, DPORT))
            print 'domain: ', domain, " send to Dns server:", ip
        except socket.error, reason:
            print reason
            continue

        '''循环接收收到的返回header'''
    while 1:
        try:
            r, w, e = select.select([s], [], [], 3)
            if not (r or w or e):
                break
            (data, addr) = s.recvfrom(65535)
            u = Lib.Munpacker(data)
            r = Lib.DnsResult(u, {})

            # print r.header
            # print r.answers
            # print r.answers[1]['data']

            if r.header['status'] == 'NOERROR' and r.header['ancount']:
                  # print r.answers
                  answer_list = []
                  for answer in r.answers:
                    # print  answer['name'],answer['data'],answer['type']
                        answer_list.append({'name':answer['name'],'data':answer['data'],'type':answer['type']})
                  result.append({'ip': addr[0], 'answer': answer_list})
                    # print r.answers[1]['data']
                    # result.append({'ip': addr[0], 'ancount': r.header['ancount']})
            else:
                  print r.header

        except socket.error, reason:
            print reason
            s.close()
            continue
        except:
            s.close()
            continue
    s.close()
    result2sql(result)


def result2sql(results):
    """
    结果存入数据库
    """
    fw = open('output.txt', 'a')

    if not results:
        return

    for res in results:
        print res
        print >> fw, res


def main():
    """
    Demo
    """
    if len(sys.argv) < 2:
        print "Wrong format ,eg. python dns_available_test ip.txt"
        sys.exit(0)

    try:
        fr_input = open(sys.argv[1], 'r')
    except:
        print 'There is  not ' + fr_input
        sys.exit(0)

    ip_list = fr_input.readlines()
    ip_list = list(set(ip_list))
    rowcount = len(ip_list)

    fr_input.close()

    count = 0
    while count * THREAD_NUM < rowcount:
        ips = ip_list[count * THREAD_NUM: (count + 1) * THREAD_NUM]
        gevent.joinall(
            [gevent.spawn(check_ip, eval(ip)['ip'].strip()) for ip in ips])
        # gevent.joinall([
        #     gevent.spawn(check_ip,ips[0][0] ),
        #     gevent.spawn(check_ip,ips[1][0] ),
        #     gevent.spawn(check_ip,ips[3][0] ),
        #     gevent.spawn(check_ip,ips[2][0] ),
        #     gevent.spawn(check_ip,ips[4][0] ),
        #     ])
        ips = []
        count = count + 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "User Press Ctrl +C,exit"
    except EOFError:
        print "User Press Ctrl +D,exit"

#!usr/bin/python
# encoding:utf-8
"""
该程序用来分析发包数量、网络拥塞情况
"""
import socket
import select
import struct
import DNS
import sys
import random
import datetime
import commands
import re
import time
from DNS import Type
from DNS import Class
from DNS import Opcode
from DNS import Lib


PACKAGE_NUM = 250   # Detect package number everytime
CYCLE_NUM = 5  # Cycle number
# Dns type
DNSSERVERTYPE = ["Authoritative Name server",
                 "Authoritative Name server(with recursive service)", "The Recursive Name Server", "unknow"]


def ip2long(ipstr):
    """
    Ip turn to Long
    """
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]


def long2ip(ip):
    """
    Long turn to Ip 
    """
    return socket.inet_ntoa(struct.pack("!I", ip))


def batch_server_detect(list_ip=[]):
    '''
    Dns detect
    '''

    # TID为随机数
    tid = random.randint(0, 65535)
    # 端口为53,UDP
    port = 53
    # 操作为查询
    opcode = Opcode.QUERY
    # Tpye类型为A
    qtype = Type.PTR
    # 查询类，一般为IN
    qclass = Class.IN
    # 期望递归
    rd = 1

    # 建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    # socket绑定到指定IP地址和接口上
    s.bind(('', source_port))

    ip_count = len(list_ip)
    count = 0
    result = []
    while count * PACKAGE_NUM < ip_count:
        ips = list_ip[count * PACKAGE_NUM: (count + 1) * PACKAGE_NUM]
        for ip in ips:

            server = long2ip(ip)

            m = Lib.Mpacker()
            m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
            ip_tips = server.split(".")
            qname = ip_tips[3] + '.' + ip_tips[2] + \
                '.' + ip_tips[1] + '.' + ip_tips[0]
            qname += '.in-addr.arpa'
            m.addQuestion(qname, qtype, qclass)
            request = m.getbuf()

            try:
                s.sendto(request, (server, port))
                # print a, "send to IP:", server
            except socket.error, reason:
                print reason

        while 1:
            try:
                r, w, e = select.select([s], [], [], 3)
                if not len(r):
                    break
                (reply, from_address) = s.recvfrom(65535)
                u = Lib.Munpacker(reply)
                r = Lib.DnsResult(u, {})
                if r.header['ra'] == 1 and r.header['aa'] == 0:
                    print from_address, "递归服务器"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[2], 'other': r.header['status']})
                elif r.header['ra'] == 1 and r.header['aa'] == 1:
                    print from_address, "权威服务器(递归服务)"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[1], 'other': r.header['status']})
                elif r.header['ra'] == 0 and r.header['aa'] == 1:
                    print from_address, "权威服务器"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[0], 'other': r.header['status']})
                else:
                    print from_address, "服务器类型探测失败：未知服务器", r.header['status']
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[3], 'other': r.header['status']})

            except socket.error, reason:
                print reason

            except DNS.Error as e:
                print e

        ips = []
        count = count + 1
    s.close()
    return result


def getPing(ip):
    xpin = commands.getoutput("ping -c 3 %s" % ip)
    ms = 'time=\d+.\d+'
    mstime = re.search(ms, xpin)
    if not mstime:
        MS = 'timeout'
        return MS
    else:
        MS = mstime.group().split('=')[1]
        return MS

def main():

    cycles = CYCLE_NUM
    fr = open(sys.argv[1], 'r')
    fw_name = sys.argv[2]
    ip_list = fr.readlines()
    lines = len(ip_list)
    fr.close()

    while cycles:

        fw = open(fw_name, 'a')
        starttime = datetime.datetime.now()
        results = []
        results_count = 0
        ipNum = 0

        for i in xrange(0, lines, 2):

            results = []
            list_ip = []
            start_ip = ip_list[i].strip()
            end_ip = ip_list[i + 1].strip()
            long_start_ip = ip2long(start_ip)
            long_end_ip = ip2long(end_ip)
            ip_count = long_end_ip - long_start_ip + 1
            ipNum = ip_count + ipNum

            for i in range(long_start_ip, long_end_ip + 1):
                list_ip.append(i)
            random.shuffle(list_ip)   # To make the ips randomly

            results = batch_server_detect(list_ip)

            results_count = len(results) + results_count
        ping = getPing('www.baidu.com')
        endtime = datetime.datetime.now()
        long_time = str((endtime - starttime).seconds)
        str_write = 'package_num:' + str(PACKAGE_NUM) + '\t' + 'ipNum:' + str(ipNum) + '\t' + 'Dns_num:' + str(results_count) + '\t' + 'start_time:' + str(starttime) \
            + '\t' + 'end_time:' + \
            str(endtime) + '\t' + 'long_time:' + \
            long_time + '\t' + 'ping:' + ping + '\n'
        fw.write(str_write)

        fw.close()
        cycles = cycles - 1
        time.sleep(30)

    print 'Dns detect finish'

if __name__ == '__main__':
    main()

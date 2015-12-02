#!usr/bin/python
#encoding:utf-8
"""
功能：计算IP段之间的IP个数
输入：txt文件，每个IP为一行，例如
                           1.12.2.3 
                           1.12.211.122
输出：IP个数

"""
import socket
import struct
import sys

def ip2long(ipstr):
    """
    Ip turn to long
    """ 
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]

def long2ip(ip):
    """
    long turn to Ip
    """ 
    return socket.inet_ntoa(struct.pack("!I", ip))

def main():

    if len(sys.argv)<2:
        print 'Wrong,format'
        sys.exit(0)
    fr = open(sys.argv[1],"r")
    ip_count = 0    
    ip_list = fr.readlines()
    lines = len(ip_list)
    if not lines:
        print 'There are not ips to detect'
        return

    for i in xrange(0,lines,2):

        start_ip = ip_list[i].strip()
        end_ip = ip_list[i+1].strip()

        try:
            long_start_ip = ip2long(start_ip)
            long_end_ip   = ip2long(end_ip)
        except:
            print 'Wrong ip format,please check it'
            continue
        ip_count = (long_end_ip - long_start_ip) + ip_count + 1
    print ip_count
    fr.close()

if  __name__ ==  '__main__':
    main()

#!/usr/bin/python
# coding:utf-8
'''
程序功能:通过网页爬虫，将网站(http://ips.chacuo.net/)上各运营商的IP段提取出，分别将保存为txt文件，并且计算出比例
输入：网站名称
输出：各省市的IP段
作者：程亚楠
时间：2015.2.6
'''
from bs4 import BeautifulSoup
import urllib2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import socket
import struct

# isp字典
isp_dic = {
    '电信宽带': 'CHINANET', '联通宽带': 'UNICOM', '移动宽带': 'CMNET', '教育网': 'CERNET', '铁通宽带': 'CRTC', '网通宽带': 'CNCGROUP', '长城宽带': 'GWBN', '中科网宽带': 'CSTN', '广电宽带': 'BCN', '歌华宽带': 'GeHua',
    '天威宽带': 'Topway', '方正宽带': 'FOUNDERBN', '中邦宽带': 'ZHONG-BANG-YA-TONG', '华数宽带(杭州)': 'WASU', '珠江宽带': 'GZPRBNET', '油田宽带': 'HTXX', '视讯宽带': 'eTrunk', '东南宽带': 'WSN', '金桥网宽带': 'CHINAGBN', '盈联宽带': 'EASTERNFIBERNET',
    '华宇宽带': 'LiaoHe-HuaYu', '有线宽带': 'CTN'
}

def ip2long(ipstr):
    """
    Ip turn to long
    """ 
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]

def extract_isp():
    for isp in isp_dic:
        print isp
        i = 1
        url = "http://ipcn.chacuo.net/view/i_" + isp_dic[isp] 
        try:
            content = urllib2.urlopen(url).read()
        except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
            print "The server couldn't fulfill the request"
            # print "Error code:",e.code
            # print "Return content:",e.read()
            continue
        except urllib2.URLError,e:    #无法得到service
            print "Failed to reach the server"
            # print "The reason:",e.reason
            # return    
            # sys.exit(0)
            continue   
        soup = BeautifulSoup(content)
        path = './ISP/' + isp
        is_path_exist = os.path.exists(path)
        if not is_path_exist:
            os.makedirs(path)
            os.makedirs(path+'/City')
        fw = open(path+'/'+isp+'.txt', 'w')

        for link in soup.find_all('dd'):
            city_name = ''
            city_name = link.previous_sibling.previous_sibling.string
            if  city_name:
                print city_name
                fw.write(city_name + '\n')
                print link.span.string
                fw.write(link.span.string + '\n')
                print link.span.next_sibling.string
                fw.write(link.span.next_sibling.string + '\n')
            else:
                for l in link.find_all('span'):
                    print l.string
                    fw.write(l.string+'\n')

        fw.close()
        print isp + '已经处理完成'


def extract_isp_city():
    
    for isp in isp_dic:
        try:
            fr  = open('./ISP/'+isp+'/'+isp+'.txt')
        except:
            print "not exsit"
            continue
        ip_list = fr.readlines()
        lines = len(ip_list)
        if not lines:
            print 'There are not ips to detect'
            continue
        for i in xrange(0,lines):
            ip = ip_list[i].strip()
            print ip
            try:
                long_ip = ip2long(ip)
            except:
                print ip
                fw = open('./ISP/'+isp+'/City/' +ip+'.txt','w')
                continue
            print ip
            fw.write(ip+'\n')

    fr.close()

def ip_count():
    for isp in isp_dic:
        print isp
        listdir = os.listdir('./ISP/' + isp +'/City/' )
        for city in listdir:
            print city
            try:
                fr = open('./ISP/'+isp +'/City/' +city,"r")
            except :
                continue
            ip_count = 0    
            ip_list = fr.readlines()
            lines = len(ip_list)
            if not lines:
                print 'There are not ips to detect'
                continue

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
            fw = open('./ISP/'+city,'a')
            fw.write(isp+'\t' + str(ip_count) + '\n')
            print ip_count
            fw.close()
            fr.close()

def main():

    extract_isp()
    extract_isp_city()
    ip_count()

    print 'All done'

if __name__ == '__main__':
    main()

#!/usr/bin/python
#coding:utf-8
'''
程序功能:通过网页爬虫，将网站(http://ips.chacuo.net/)上各省市的IP段提取出，并且分别将省市保存为txt文件
输入：网站名称
输出：各省市的IP段
作者：程亚楠
时间：2015.2.6
'''
from bs4 import BeautifulSoup
import urllib2
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os

path = './IpSource/'
is_path_exist = os.path.exists(path)
if not is_path_exist:
    os.makedirs(path)

#City字典
cityip = {
                 '北京':'BJ','广东':'GD','山东':'SD','浙江':'ZJ','江苏':'JS','上海':'SH','辽宁':'LN','四川':'SC','河南':'HA','湖北':'HB',
                 '福建':'FJ','湖南':'HN','河北':'HE','重庆':'CQ','山西':'SX','江西':'JX','陕西':'SN','安徽':'AH','黑龙江':'HL','广西':'GX',
                 '吉林':'JL','云南':'YN','天津':'TJ','内蒙古':'NM','新疆':'XJ','甘肃':'GS','贵州':'GZ','海南':'HI','宁夏':'NX','青海':'QH',
                 '西藏':'XZ','香港':'HK'
                 }
for city in cityip:
    print city
    url = "http://ips.chacuo.net/view/s_"+cityip[city]

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
    fp = open('./IpSource/' + city + '.txt','w')
    for link in soup.find_all('span'):
        if  link.string  =='请输入地址':
            continue
        else:
            fp.write(str(link.string) + '\n')
        
    fp.close()
    print city+'已经处理完成'
print '所有城市处理完成'
    

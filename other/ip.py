#encoding:utf-8
"""
将DNS探测结果中的IP提取出来，保存到txt文件中，每个ip为一行
"""
import MySQLdb
import sys

result_path = sys.argv[1]
fr = open(result_path,'r')
fw = open('ip.txt','w')

dns_list = fr.readlines()
print type(dns_list)
l2 = list(set(dns_list))
print len(dns_list)
print len(l2)
for ip in dns_list:
	print ip,
        fw.write(eval(ip)['ip'].strip()+'\n')

fr.close()
fw.close()

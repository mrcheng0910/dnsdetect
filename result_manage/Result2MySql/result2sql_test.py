#encoding:utf-8
"""
将探测到的数据保存到数据库中
"""
import MySQLdb
import sys

conn=MySQLdb.Connection(host='localhost',user='root',passwd='cynztt',db='dns_detect',charset='utf8')
cursor = conn.cursor()


result_path = sys.argv[1]



fr = open(result_path,'r')
dns_list = fr.readlines()

for ip in dns_list:
	print ip,
	sql = 'INSERT ignore INTO test(ip,type,status) VALUES(%s,%s,%s)'
	cursor.execute(sql,(eval(ip)['ip'].strip(),eval(ip)['type'].strip(),eval(ip)['other'].strip()))

conn.commit()
fr.close()

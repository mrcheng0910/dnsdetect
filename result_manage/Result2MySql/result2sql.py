#encoding:utf-8
"""
将探测到的数据保存到数据库中
"""
import MySQLdb
import sys

conn=MySQLdb.Connection(host='localhost',user='root',passwd='cynztt',db='dns_detect',charset='utf8')
cursor = conn.cursor()
if len(sys.argv)<6:
    print 'wrong format'
    print 'python result.txt ip_isp node_region node_isp detect_times'
    sys.exit(0)

result_path = './ResultData/' + sys.argv[1]
ip_isp = sys.argv[2]
node_region = sys.argv[3]
node_isp = sys.argv[4]
detect_times = sys.argv[5]


fr = open(result_path,'r')
dns_list = fr.readlines()

for ip in dns_list:
	print ip,
	sql = 'INSERT INTO detect_result_shanghai(ip,type,status,ip_isp,node_region,node_isp,detect_times) VALUES(%s,%s,%s,%s,%s,%s,%s)'
	cursor.execute(sql,(eval(ip)['ip'].strip(),eval(ip)['type'].strip(),eval(ip)['other'].strip(),ip_isp,node_region,node_isp,detect_times))

conn.commit()
fr.close()

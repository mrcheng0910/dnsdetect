#encoding:utf-8
"""
访问亚太网络信息中心(APNIC)，查询ip地址
"""
from socket import *
  
HOST = '202.12.29.220' 
PORT = 43
BUFSIZ = 1024  
ADDR = (HOST, PORT)
EOF="\r\n"  
request_ip="117.101.51.226"
data_send=request_ip+EOF
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
tcpCliSock.send(data_send)
while True:
    data_rcv = tcpCliSock.recv(BUFSIZ)  
    if not len(data_rcv):
        break    
    print data_rcv.encode("GBK")
  
tcpCliSock.close()
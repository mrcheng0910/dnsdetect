#!/usr/bin/env python
# encoding: utf-8

import Lib
import random
import socket
import select
import Type
import Class
import Opcode

def detect():
    tid = random.randint(0,65535)

    port = 53
    server = '202.102.154.3'
    opcode = Opcode.QUERY
    qtype = Type.A
    qclass = Class.IN
    qname = "google.com"
    rd = 1

    m = Lib.Mpacker()
    m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
    m.addQuestion(qname,qtype,qclass)

    request = m.getbuf()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    s.bind(('', source_port))
    s.connect((server,port))

    s.send(request)

    r,w,e = select.select([s], [], [],timeout=1)
    if not len(r):
        print "time out"
    (reply, from_address) = s.recvfrom(65535)

    u = Lib.Munpacker(reply)
    r = Lib.DnsResult(u,{})

    print r.answers

if __name__ == "__main__":
    detect()


#!/usr/bin/expect -f

set timeout -1
set password "50234327"
#set dir1 [lindex $argv 1]
#set dir2 [lindex $argv 2]
spawn scp -r root@58.221.45.223:cyn/DnsDetect/DnsResult ./
#spawn scp -r root@58.221.45.223:cyn/DnsAnalysis/ ./
expect {
"*yes/no" {send "yes\r"; exp_continue}
"*password:" {send "$password\r"}
}
expect eof

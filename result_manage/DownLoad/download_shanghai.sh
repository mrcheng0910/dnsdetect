#!/usr/bin/expect -f

set timeout -1
set password "68(yqTc%"
#set dir1 [lindex $argv 1]
#set dir2 [lindex $argv 2]
spawn scp -r root@139.159.35.200:cyn/DnsDetect/DnsResult ./
#spawn scp -r root@139.159.34.80:cyn/DnsAnalysis ./
expect {
"*yes/no" {send "yes\r"; exp_continue}
"*password:" {send "$password\r"}
}
expect eof

## 项目简介
### ip_count.py
* **功能：**该程序用来查询输入Ip段中IP的个数
* **输入：**输入为.txt文件，文件格式如下：          		
                 1.1.1.1   
                 1.2.255.255   
                  ......   
* **输出：** IP段含有IP个数

### ip.py
* **功能：**该程序将Dns探测结果中ip提取出，并且每行为一个ip的格式存入ip.txt文件
* **输入：**Dns探测结果
* **输出：**dns_result.txt
* **命令格式：**python ip.py 

### ip_location.py
* **功能：**该程序通过在线调用淘宝API，对IP进行定位
* **输入:**Ip
* **输出：**国家，省份，城市，ISP

### result_compare.py
* **功能：**该程序比较DNS探测结果的交集，并集，差集

### apnicip.py
* **功能：**This programe detects the location of ips with apnic api


#### 一，项目文件介绍
	1、DNS为库文件
	2、IpSource存放输入文件
	3、DnsResult存放探测结果
	4、config.py为配置文件
	5、dns_verify.py为程序运行文件
	6、ReadMe.md为项目简介

#### 二，程序功能
	对已经获得的Dns探测结果进行再次确认

#### 三，输入数据
	1. 输入文件格式为txt文件，在IpSource文件夹中
	2. 程序通过读入Dns段进行探测
	3. 其中config.py配置文件，用来配置程序每次发包次数以及超时时间，默认每次发包5000,超时时间为3秒

#### 四，输出数据
	输出结果文件保存在DnsResult文件夹中，其中有两类文件
	1、.txt文件为探测结果文件，包含是DNS服务器的数据
	2、Run.log文件，保存本次探测详细，包括运行时间，探测DNS个数，IP个数等信息

#### 五，运行环境
	1、运行环境Linux,python2.7即可
	2、运行dns\_verify.py  运行命令：python dns\_verify.py input.txt output
	其中，input.txt为输入文件（保存在IpSource中），输出文件为output_***.txt（保存在DnsResult中）,其中***为程序运行时间，会自动添加

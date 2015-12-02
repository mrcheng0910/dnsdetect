#### 一，项目文件介绍
	1、DNS为库文件
	2、shanghai_unicom.txt存放输入文件
	3、dns_analysis.py为程序运行文件
	4、ReadMe.md为项目简介

#### 二，程序功能
	通过组包发送DNS查询报文，判断所探测IP是否为DNS服务器,通过循环分析，检测服务器的一天的网络质量，程序运行时间和探测结果作出分析。

#### 三，输入数据
	1、输入文件格式为txt文件
	2、程序通过读入IP段进行探测
	3、数据格式如下：
	      121.12.0.0 
	      121.13.255.255
	      ......

#### 四，输出数据
	1、.txt文件为探测结果文件，包含本次探测IP数量，DNS数量等信息

#### 五，运行环境
	1、运行环境Linux,python2.7即可
	2、运行dns\_analysis.py  运行命令：python dns_analysis.py input.txt output.txt，input.txt为输入文件名，output.txt为输出文件名，保存结果

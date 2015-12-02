## 项目简介
### Collect_City_Ip.py
* **功能：**通过爬虫，获取各个省份城市的IP段
* **运行：**运行环境与命令
    + **环境：**Ubuntu，Python2.7
    + **命令：**python Collect\_City\_Ip.py
* **输出：**在IpSource目录中生成结果文件

### Collect_ISP_Ip.py
* **功能：**通过爬虫，获取各个运营商在省市中IP的分布以及数量
* **运行：**运行环境与命令
    + **环境：**Ubuntu，Python2.7
    + **命令：**python Collect\_ISP\_Ip.py
* **输出：**在IpSource目录中生成结果文件  

### IpSource目录
* **内容：**该目录中存放全国各个省份城市的IP段，可以直接作为DNS分布探测的输入

### ISP目录
* **内容：**该目录中存放各个运营商在各个省份城市中所使用IP段，以及各个城市中各个运营商的数量

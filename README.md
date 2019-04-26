# zufang
根据用户输入的上班地址,价格区间,返回现有满足条件中介所有租房信息,

## 包含到指定地点的公共交通的最短时间!!!

大学毕业面临找实习,就得租房,突发奇想

### ProxyPool:
利用redies维护的动态IP代理池,供给爬虫做代理

### scrapy_woaiwojia
利用scrapy(用到的不多,感觉性能欠佳,还在边学边摸索),爬取我爱我家租房信息

### location
先申请一个高德地图的API(百度API竟然收费!),然后将自己的key更换上去,就可以愉快的等待结果了.
1.用户传入目标地址,价格区间
2.循环读取数据库中的租房房源信息
3.将读取的房源地址作为目的地址,同目标地址一同转换为经纬度坐标
4.将经纬度坐标通过高德API查询两地间,公共交通所需的最短时间
5.通过对公共交通时间的排序,最后输出房源ID信息,可到官网查询具体信息


PS:边学边随手写的小代码.慢慢增加功能

样例:
./test.png

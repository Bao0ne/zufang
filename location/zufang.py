from conn import *
from duration import durations

def res(origin, price_min, price_max):
    #起点,用户给定
    #origin
    #终点
    destination = ''

    #最低价格
    #price_min = 0
    #最高价格
    #price_max = 0

    #计数君
    count = 0

    #先通过价格进行筛选
    items = filter(price_min , price_max)   #返回的是二维元组
    #items = list(items)
    #想要将结果根据duration 从小到大排序
    res_list = []

    for item in items:
        #取到终点地址
        item = list(item)
        title = item[0]
        price = item[1]
        area = item[2]
        metro = item[3]
        href = item[4]
        destination = area

        # 两地之间预期时间
        duration = durations(origin, destination)
        item[14] = duration
        m, s = divmod(int(duration), 60)
        h, m = divmod(m, 60)
        item[15] = '%d:%02d:%02d' % (h, m, s)
        res_list.append(item)
        #print("房子的ID:%s"%href + '-----------' +"公共交通所需时长为:%d:%02d:%02d" % (h, m, s))
        count += 1
    res_sorted = sorted(res_list, key=lambda x: x[14])
    for r in res_sorted:
        print('目标地址:%s'%origin)
        print('房源ID:%s'%(r[4]))
        print('房源位置:%s'%(r[2]))
        print('公共交通预期时长为:%s'%(r[15]))
        print('房源租金:%s'%(r[1]) + '元/月')
        print('地铁相关信息:%s'%(r[3]))
        print('----------------------------------------------------------------')
    print('共搜索到%s套符合条件的房源'%count)


















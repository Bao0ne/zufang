from zufang import res
import time

#开始时间
start_time = time.time()


#入口文件
origin = '大望路地铁站'
price_min = 2700
price_max = 3000
res(origin, price_min, price_max)

#结束时间
stop_time = time.time()

#运行时间
running_time = stop_time - start_time
print('共运行时长%s'%running_time + 's')





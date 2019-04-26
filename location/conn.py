import pymysql

def filter(price_min ,price_max):
    #通过price区间筛选符合条件的条目
    # price_min = 1000   #最低价格
    # price_max = 3000   #最高价格

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "house")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM woaiwojia_zufang WHERE price > %d and price < %d"%(price_min ,price_max)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0])
        # for row in results:
        #     title = row[0]
        #     price = row[1]
        #     area = row[2]
        #     metro = row[3]
        #     href = row[4]
        #     # 打印结果
            #print("title=%s,price=%s,area=%s,metro=%s,href=%s" %(title, price, area, metro, href))
    except:
        print("Error: unable to fetch data")

    #关闭游标
    cursor.close()
    # 关闭数据库连接
    db.close()
    return results

#filter(1000, 3000)
















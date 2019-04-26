import requests
import json

def durations(origin, destination):
    #查询两位置的经纬度及公共交通的最短预期时间

    #起点
    #origin
    #终点
    #destination
    #print('起点:%s'%origin)
    #print('终点:%s'%destination)

    # 高德地图API
    url_l1 = 'https://restapi.amap.com/v3/geocode/geo?key=<你的key>0&output=JSON&address=%s&city=北京'%origin
    url_l2 = 'https://restapi.amap.com/v3/geocode/geo?key=<你的key>&output=JSON&address=%s&city=北京'%destination

    resp_l1 = requests.get(url_l1)
    resp_l2 = requests.get(url_l2)

    #获取地位置经纬度
    # print(response.status_code)
    # print(response.text)
    js1 = json.loads(resp_l1.text)
    #print(type(js))
    location1 = js1.get('geocodes')[0].get('location')
    #print('起点坐标地址: %s'%location1)

    # print(response2.status_code)
    # print(response2.text)
    js2 = json.loads(resp_l2.text)
    location2 = js2.get('geocodes')[0].get('location')
    #print('终点坐标地址: %s'%location2)

    #获取公共交通时间,路线
    #https://restapi.amap.com/v3/direction/transit/integrated?origin=116.481499,39.990475&destination=116.465063,39.999538&city=010&output=xml&key=<用户的key>

    #json
    url_com_json = 'https://restapi.amap.com/v3/direction/transit/integrated?origin=%s&destination=%s&city=北京&strategy=0&output=json&key=<你的key>'%(location1, location2)
    #print(url_com_json)

    resp_com = requests.get(url_com_json)
    js_com = json.loads(resp_com.text)

    #预期时间
    duration = js_com.get('route').get('transits')[0].get('duration')
    #print('预期时间为:' + duration + 's')
    return duration
























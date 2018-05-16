#coding:utf-8
import os
import random
import requests
import time
import threading as t

proxy_ip_list = []
read_count=0
url = 'https://blog.csdn.net/zach_z/article/details/'
arts = ['80296081', '80293342', '80273392', '80199389', '80188764', '80153536', '80115234', '80111542', '80102219', '80087986',
        '80086523', '80084121', '80082957', '80072929', '80072906', '80045105',
        '80045093', '80045085', '80045081', '80029826', '79823605', '79721164',
        '79619400', '79576090', '79443773', '79394863', '79383305', '79372822',
        '79307910', '79212688', '79201373', '79157305', '79118042', '79023906',
        '78946699', '78916441', '78826429', '78825684', '78787509', '78611935',
        '78588362', '78578631', '78576384', '78576216', '78574810', '78529804',
        '78426782', '78409689', '78377754', '78370531', '78353188', '78221431',
        '78199119', '78171329', '78167944', '78159843', '78015138', '78012325',
        '77992783', '77972759', '72820633', '77923874', '77893438', '77855977',
        '77621885', '77620708', '77571919', '77515372', '77493299', '77435898',
        '77413878', '77394523', '77280006', '77170612', '76651137', '75913295',
        '75807478', '75660761', '75579688', '75331275', '75213676', '75213645',
        '75213642', '75213639', '75095061', '73455506', '73196132', '72902591',
        '72840409', '72820667', '72784369', '72620205', '71511876', '71437238',
        '71132681', '70949435', '70885704', '70851717', '70821441', '70745583',
        '70727713', '70226897', '70215342', '70214354', '69258244', '68070552',
        '66973342', '53648611']

#此处修改头字段,自己用f12查看谷歌浏览器下自己的浏览器头信息，可以让根据目标站点而写的head会更好
headers = {
    'Host':"blog.csdn.net",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
def load_list_from_file(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        #print(data_list)
        return data_list
def get_proxy_ip():
    global proxy_ip_list
    list_len = len(proxy_ip_list)
    if not list_len == 0:
        ip = proxy_ip_list[random.randint(0, list_len - 1)]
        return {
            'http': 'http://' + ip,
	    'https': 'https://' + ip
        }
def get_request(url,headers):
    for x in range(len(proxy_ip_list)):
        ip = proxy_ip_list[x]
        proxies={
            'http': 'http://' + ip,
	    'https': 'https://' + ip
        }
        try:
            global read_count
            html=requests.get(url,headers=headers, timeout=10,proxies=proxies).text
            time.sleep(10)
            read_count +=1
            print ("累计成功访问次数： %d" % read_count)
        except Exception as e:
            continue
    return html

# 阅读量访问线程
class Reader(t.Thread):
    def __init__(self, t_name, t_num,func):
        self.func = func
        self.num=t_num
        t.Thread.__init__(self, name=t_name)

    def run(self):
        self.func(self.num)


# 阅读操作
def reading(num):
    while True:
        urlx = url+arts[num]                
        get_request(urlx,headers)

if __name__ == '__main__':
    proxy_ip_list = load_list_from_file("./IP.txt")
    for x in range(len(arts)):
        reader = Reader("线程" + str(x), x, reading)
        reader.start()
                        

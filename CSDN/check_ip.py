import os
import requests

url='https://www.baidu.com/'
headers = {
    'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 '
                  'Safari/537.36 '
}
def load_list_from_file(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        #print(data_list)
        return data_list
    
def write_str_data(content, file_path, mode="a+"):
    with lock:
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content + "\n", )
        except OSError as reason:
            print(str(reason))
            
def get_request(url,headers):
    proxy_ip_list = load_list_from_file("./proxy_ip1.txt")
    for x in range(len(proxy_ip_list)):
        ip = proxy_ip_list[x]
        proxies={
            'http': 'http://' + ip,
	    'https': 'https://' + ip
        }
        try:
            global read_count
            html=requests.get(url,headers=headers, timeout=3,proxies=proxies).text
            read_count +=1
            write_str_data(ip,"./IP_TRUE.txt")
        except Exception as e:
            print (e)
    return html

if __name__ == '__main__':
    get_request(url,headers)

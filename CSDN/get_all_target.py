import requests
import re
from bs4 import BeautifulSoup


url_list_base='https://blog.csdn.net/Zach_z/article/list/'

target_list=[]

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def getTarget(lst,targetURL):
    html = getHTMLText(targetURL)
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('h4')
    for i in a:
        try:
            h=i.find('a')
            href=h.attrs['href']
            lst.append(re.findall(r"\d{8}",href)[0])
        except:
            continue
def getAllTarget(lst,baseURL):
    for i in range(1,7):
        targetURL=url_list_base+str(i)+'?'
        getTarget(lst,targetURL)
if __name__ == '__main__':
    getAllTarget(target_list,url_list_base)
    print(target_list)

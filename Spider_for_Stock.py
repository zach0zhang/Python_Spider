#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 21:52:49 2018

@author: zach0zhang
"""

import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
    
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, "GB2312")
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz][36]\d{5}", href)[0])
        except:
            continue
        
def getStockInfo(lst, stockURL, fpath):
    Listtitle=['名称','总市值','净资产','净利润','市盈率','市净率','毛利率','净利率','ROE']
    with open(fpath,'w',encoding='utf-8') as f:
        for i in range(len(Listtitle)):
            f.write("{0:<10}\t".format(Listtitle[i],chr(12288)))
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url,"GB2312")
        try:
            if html=="":
                continue
            List=[]
            soup = BeautifulSoup(html, 'html.parser')
            stock = soup.find('div',attrs={'class':'cwzb'}).find_all('tbody')[0]
            name=stock.find_all('b')[0]
            List.append(name.text)
            keyList = stock.find_all('td')[1:9]
            for i in range(len(keyList)):
                List.append(keyList[i].text)
            with open(fpath,'a',encoding='utf-8') as f:
                f.write('\n')
                for i in range(len(List)):
                    f.write('{0:<10}\t'.format(List[i],chr(12288)))
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
            continue

def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'http://quote.eastmoney.com/'
    output_file = './Stock.txt'
    slist=[]
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()
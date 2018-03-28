#!/usr/bin/python
# -*- coding: utf-8 _-*-

from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup

search = input("你想要翻译什么：")
key = {"q": search}

url = "https://cn.bing.com/dict/search?" + urlencode(key)
# print(url)

response = urlopen(url)
html = response.read().decode("UTF-8")
# print(html)

bs = BeautifulSoup(html, "html.parser")
def_lis = bs.select("div.qdef > ul > li")
results = [def_li.text for def_li in def_lis]
if results[len(results)-1][0:2] == "网络":
    results[len(results) - 1] = results[len(results)-1][0:2] + " " + results[len(results)-1][2:]
for result in results:
    print(result)

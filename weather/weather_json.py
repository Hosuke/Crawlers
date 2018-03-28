from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

url = "http://www.weather.com.cn/weather/101010100.shtml"

response = urlopen(url)

bs = BeautifulSoup(response, "html.parser")

# 按照顺序依次找出五列数据：   日期date， 描述 desc,  温度temp    风向direction  level 风力
date_list = bs.select("li > h1")
desc_list = bs.select("li > p.wea")
temp_list = bs.select("li > p.tem")
direction_list = bs.select("li > p.win > em")
level_list = bs.select("li > p.win > i")

result_list = []
for i in range(len(date_list)):
    date = date_list[i].text
    desc = desc_list[i].text
    temp = temp_list[i].stripped_strings
    temp = "".join(temp)
    direction_temp = direction_list[i]
    two_span_list = direction_temp.select("span")
    if len(two_span_list) == 1:
        direction = two_span_list[0].get("title")
    else:
        direction = two_span_list[0].get("title") + "-" + two_span_list[1].get("title")
    level = level_list[i].text
    result_list.append({"date": date, "desc": desc, "temp": temp, "direction": direction, "level": level})

for result in result_list:
    print(result)

with open("/Users/Hosuke/Developer/Python/Projects/firstpy/weather.json", "w", encoding="utf-8") as f:
    json.dump(result_list, f, ensure_ascii=False)

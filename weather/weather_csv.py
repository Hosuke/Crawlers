from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

url = "http://www.weather.com.cn/weather/101010100.shtml"

response = urlopen(url)

bs = BeautifulSoup(response, "html.parser")


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
    direction = direction_list[i]
    spans = direction.select("span")
    direction = spans[0].get("title") + "-" + spans[1].get("title")
    level = level_list[i].text
    result_list.append([date, desc, temp, direction, level])

for result in result_list:
    print("\t".join(result))


with open("/Users/Hosuke/Developer/Python/Projects/firstpy/weather.csv", mode="w", encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(result_list)
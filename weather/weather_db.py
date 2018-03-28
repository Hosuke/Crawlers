#!/usr/bin/python
# -*- coding: utf-8 -*-


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

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
    result_list.append([date, desc, temp, direction, level])
    # print(date, desc, temp,direction,level, sep="\t")

for result in result_list:
    print("\t".join(result))

'''

创建数据库表要准备的操作：
create database if not exists spider;
use spider;
create table t_weather (
    id int primary key auto_increment,
    t_date varchar(100),
    t_descc varchar(100),
    t_temp varchar(100),
    t_direction varchar(100),
    t_level varchar(100)
);
show tables;
select * from t_weather;

'''

con = pymysql.connect(host="localhost", user="root", password="hosuke", database="spider", charset='utf8', port=3306)

# 游标。  作用 就等同于  JDBC 中的 Statement
cursor = con.cursor()

for record in result_list:
    print(record)
    sql_insert = "insert into t_weather (t_date, t_descc, t_temp, t_direction, t_level) values (%s, %s, %s, %s, %s)"
    cursor.execute(sql_insert, record)

# 在这里，最开始使用了  cursor 进行了提交，这是不对的。应该使用 con.commit()
# cursor.commit()
con.commit()

cursor.close()

con.close()

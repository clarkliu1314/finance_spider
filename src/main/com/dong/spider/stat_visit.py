"""
使用Python爬虫爬取自己博客统计不同的博客的浏览量
"""
import json
import re
import sys

import pymysql
import requests

from com.dong.entity.Visit import Visit
# from com.dong.utils.DbPoolUtil import dbpool


def parse_page_index(html):
    pattern = re.compile(
        'article-item-box.*?daerzei/article/details/(.*?)".*?阅读数：(.*?)</span>.*?评论数',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield{
            Visit(None, item[0].strip(), item[1])
        }


def write_to_json(content):
    """
    将提取的结果写入文件，这里直接写入到一个文本文件中，通过json库的dumps()方法
    实现字典的序列化，并指定ensure_ascii参数为False，这样可以保证输出的结果是
    中文形而不是Unicode编码
    :param content:
    :return:
    """
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False, ) + '\n')


def visit_write_to_mysql(visit):
    db = pymysql.connect(
        host='caoweidong.cn',
        user='wedo',
        password='2708poem',
        port=3306,
        db='wedo',
        charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(visit.insert_sql())
    db.commit()
    db.close()


def main():
    if sys.platform.__eq__("linux"):
        file_path = "/opt/data/myblog/daerzei.html"
    elif sys.platform.__eq__("win32"):
        file_path = "D:\\0WorkSpace\\atom\\myblog\\daerzei.html"
    else:
        return

    with open(
            file_path,
            'r',
            encoding='utf-8'
    ) as html_src:
        content = html_src.read()

    visits = parse_page_index(content)

    for visit_set in visits:
        for visit in visit_set:
            # write_to_json(visit)
            print(visit.__str__())
            # dbpool.execute_iud(visit.insert_sql())
            # visit_write_to_mysql(visit)


if __name__ == "__main__":
    #
    main()


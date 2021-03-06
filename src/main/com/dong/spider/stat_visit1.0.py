"""
使用Python爬虫爬取自己博客统计不同的博客的浏览量
升级版
"""
import json
import re

import requests

from com.dong.entity.Visit import Visit
from com.dong.utils.DbPoolUtil import dbpool


def parse_page_index(html):
    pattern = re.compile(
        'article-item-box.*?daerzei/article/details/(.*?)".*?阅读数：(.*?)</span>.*?评论数',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield Visit(None, item[0].strip(), item[1])


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


def main():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        ),
        "Referer": "https://blog.csdn.net/"
    }
    main_page = "https://blog.csdn.net/daerzei"
    url_template = "https://blog.csdn.net/daerzei/article/list/{page}"
    visit_data = []
    for index in range(4):
        if index == 0:
            url = main_page
            headers['Referer'] = main_page
        else:
            headers['Referer'] = url_template.format(page=str(index))
            index = index + 1
            url = url_template.format(page=str(index))

        # print("url = %s" % url)
        # print("headers = %s" % headers)

        response = requests.get(url, headers=headers)
        visits = parse_page_index(response.text)

        for visit in visits:
            print(visit.insert_sql())
            visit_data.append(visit.__data__())
    # print("len(data) = %s" % len(visit_data))
    # print(visit_data)
    dbpool.execute_many_iud(Visit.insert_temple, visit_data)


if __name__ == "__main__":
    #
    main()


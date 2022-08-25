import time

import requests
import re
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63"
}


def main(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    content = resp.text

    obj = re.compile(r'<li>.*?<em class="">(?P<index>.*?)</em>.*?'
                     r'<img.*?src="(?P<image>.*?)".*?'
                     r'<span class="title">(?P<title>.*?)</span>.*?'
                     r'<br>(?P<year>.*?)&nbsp;.*?'
                     r'property="v:average">(?P<rating>.*?)</span>.*?'
                     r'<span>(?P<vote>.*?)人评价</span>.*?'
                     r'class="inq">(?P<info>.*?)</span>', re.S)
    result = obj.finditer(content)
    f = open("douban.csv", mode='a', encoding='utf-8')
    csvwriter = csv.writer(f)
    for item in result:
        data = item.groupdict()
        data['year'] = data['year'].strip()
        csvwriter.writerow(data.values())
    f.close()


if __name__ == '__main__':
    for i in range(0, 10):
        url = f"https://movie.douban.com/top250?start={i * 25}&filter="
        main(url)
        time.sleep(3)
    print("all over!!!")

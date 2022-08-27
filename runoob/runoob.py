'''
将www.runoob.com制作成离线pdf
'''

import os
import re
from urllib.parse import urlparse

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <style>
        a {
            color: #4ea1db;
            text-decoration: none;
        }
        hr {
           display: none;
        }
        pre {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            background: #fff !important;
            border-left-width: 1px !important;
        }
    </style>
</head>
<body>
{content}
</body>
</html>
"""

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70"
}

start_url = 'https://www.runoob.com/python3/python3-tutorial.html'
# start_url = 'https://www.runoob.com/go/go-tutorial.html'
domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))
filename = f'{start_url.split("/")[-1].split(".")[-2]}.pdf'


def process_img(m):
    if m.group(1).startswith("//"):
        return f'<img src="https:{m.group(1)}"/>'
    else:
        return f'<img src="{m.group(1)}"/>'


def make_pdf(url_list):
    file_list = []
    for url in url_list:
        resp = requests.get(url, headers=headers)
        resp.encoding = 'UTF-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        body = soup.find('div', class_='article-body')
        quiz_tag = body.find('div', attrs={'id': 'quiz'})
        if quiz_tag is not None:
            quiz_tag.decompose()
        result = html_template.replace("{content}", str(body))
        obj = re.compile(r'<img.*?src="(.*?)".*?>', re.S)
        result = obj.sub(process_img, result)
        file_name = url.split("/")[-1].split(".")[-2]
        with open(f'{file_name}.html', 'w', encoding='utf-8') as f:
            f.write(result)
        file_list.append(f'{file_name}.html')
    try:
        pdfkit.from_file(file_list, filename)
    except Exception as e:
        print(e)

    for file in file_list:
        if os.path.exists(file):
            os.remove(file)


def parse_url_list():
    resp = requests.get(start_url, headers=headers)
    resp.encoding = 'UTF-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    menus = soup.select('div[id~=leftcolumn]>a')
    url_list = []
    for a in menus:
        if a['href'].startswith("/"):
            url_list.append(f"{domain}{a['href']}")
        else:
            url_list.append(f"{domain}/{start_url.split('/')[-2]}/{a['href']}")
    return url_list


if __name__ == '__main__':
    url_list = parse_url_list()
    make_pdf(url_list)

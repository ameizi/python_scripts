'''
将www.tutorialspoint.com制作成离线pdf
'''

import re
import os
import pdfkit
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <link rel="stylesheet" href="https://www.tutorialspoint.com/static/css/custom.css?v=8.000120">
    <style>
        a {
            color: #4ea1db;
            text-decoration: none;
        }
        body {
            padding: 10px;
            background-color: #fff;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0 0 24px;
            padding: 8px 8px 8px 8px;
            border: none;
        }
        .prettyprint{
            width: auto;
        }
        .demo-view{
            display: none;
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

domain = 'https://www.tutorialspoint.com'


def process_img(m):
    if not m.group(1).startswith("https"):
        return f'<img src="{domain}{m.group(1)}"/>'
    else:
        return f'<img src="{m.group(1)}"/>'


def make_pdf(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.find('div', attrs={'id': 'mainContent'})
    content.find('hr').decompose()
    content.find('div', attrs={'id': 'google-top-ads'}).decompose()
    content.find('div', class_='mui-container-fluid button-borders').decompose()
    load_div = content.find('div', attrs={'id': 'load'})
    if load_div is not None:
        load_div.decompose()
    content.find('div', attrs={'id': 'bottom_navigation'}).decompose()
    content.find('div', attrs={'id': 'google-bottom-ads'}).decompose()
    result = html_template.replace("{content}", str(content))
    obj = re.compile(r'<img.*?src="(.*?)".*?>', re.S)
    result = obj.sub(process_img, result)
    file_name = url.split("/")[-1].split(".")[-2]
    with open(f'{file_name}.html', 'w', encoding='utf-8') as f:
        f.write(result)
    pdfkit.from_file(f'{file_name}.html', f'{file_name}.pdf')
    if os.path.exists(f'{file_name}.html'):
        os.remove(f'{file_name}.html')


if __name__ == '__main__':
    urls = [
        'https://www.tutorialspoint.com/java_technology_tutorials.htm',
        "https://www.tutorialspoint.com/python_technologies_tutorials.htm",
        "https://www.tutorialspoint.com/big_data_tutorials.htm"
    ]
    for url in urls:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        md3 = soup.select('div[class~=course-box]>a')
        parse_url_list = [
            f"{domain}/{a['href'].split('/')[-2]}" \
            f"/{a['href'].split('/')[-2]}_quick_guide.htm" for a in
            md3]
        with ThreadPoolExecutor(max_workers=8) as pool:
            pool.map(make_pdf, parse_url_list)
        pool.shutdown()

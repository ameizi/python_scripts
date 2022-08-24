from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import pdfkit
import os
import re

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>{title}</h1>
{content}
</body>
</html>
"""

target = [
    {"廖雪峰Python.pdf": "https://www.liaoxuefeng.com/wiki/1016959663602400"},
    {"廖雪峰Git.pdf": "https://www.liaoxuefeng.com/wiki/896043488029600"},
    {"廖雪峰Java.pdf": "https://www.liaoxuefeng.com/wiki/1252599548343744"},
]

htmls = []


def parse_body(index, url):
    '''
    解析正文
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find('h4').get_text()
    body = soup.find_all(class_="x-wiki-content")[0]

    # 修改body中img标签图片路径，由相对路径修改为绝对路径
    def func(m):
        if not m.group(1).startswith("https"):
            scheme = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))
            return f'<img src="{scheme}{m.group(1)}"/>'
        else:
            return f'<img src="{m.group(1)}"/>'

    obj = re.compile(r'<img.*?data-src="(.*?)".*?/>', re.S)
    content = obj.sub(func, str(body))
    content = html_template.format(title=title, content=content)
    file_name = f"{str(index)}.html"
    with open(file_name, 'w') as f:
        f.write(content)
    htmls.append(file_name)


def parse_menu(url):
    """
    解析所有URL目录列表
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    urls = []
    for a in menu_tag.find_all("a"):
        urls.append(f"https://www.liaoxuefeng.com{a.get('href')}")
    return urls


def save_pdf(file_name, htmls):
    """
    把所有html文件转换成pdf文件
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip'),
            ("User-Agent",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63")
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, file_name, options=options)


if __name__ == '__main__':
    for item in target:
        for file_name, start_url in item.items():
            urls = parse_menu(start_url)
            for index, url in enumerate(urls):
                parse_body(index, url)
            try:
                save_pdf(file_name, htmls)
            except Exception as e:
                print(e)
            for html in htmls:
                os.remove(html)

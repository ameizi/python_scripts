'''
使用Python将CSDN博客制作成PDF电子书
pip install requests
pip install beautifulsoup4
pip install pdfkit
'''

from bs4 import BeautifulSoup
import requests
import pdfkit
import os

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <style>
        a {
            color: #4ea1db;
            text-decoration: none;
        }
        .pre-numbering {
            display: none;
        }
        img {
            max-width: 95%;
        }
        body {
            padding: 10px;
            max-width: 95%;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #1d1f21;
            margin: 0 0 24px;
            padding: 8px 8px 8px 8px;
            border: none;
        }
        pre code {
            font-size: 14px;
            line-height: 22px;
        }
        .prism-tomorrow-night .prism {
            background: #1d1f21;
            color: #c5c8c6;
        }
    </style>
</head>
<body>
<h1>{title}</h1>
{content}
</body>
</html>
"""

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63"
}

if __name__ == '__main__':
    htmls = []
    urls = [
        "https://blog.csdn.net/networken/article/details/124071068",
        "https://blog.csdn.net/networken/article/details/126295863",
        "https://blog.csdn.net/networken/article/details/126321152",
    ]
    for index, url in enumerate(urls):
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.content, "html.parser")
        # 获取body
        body = soup.find('div', id='content_views')
        # 查找第一个h2标签
        h2 = body.find('h2')
        # 取出标题
        title = h2.get_text()
        # 移除掉第一个h2标签
        h2.decompose()
        # 转化为字符串
        content = str(body)
        # 内容替换
        content = html_template.replace('{title}', title).replace('{content}', content)
        file_name = f'{index}.html'
        with open(file_name, 'w') as f:
            f.write(content)
        htmls.append(file_name)

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

    try:
        pdfkit.from_file(htmls, "CSDN.pdf", options=options)
        # pdfkit.from_file(htmls, "CSDN.pdf")
    except Exception as e:
        print(e)
    for html in htmls:
        os.remove(html)

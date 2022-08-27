import re
from concurrent.futures import ThreadPoolExecutor

import requests

urls = [
    'https://www.python.org/',
    'https://www.jd.com/',
    'https://www.baidu.com/',
    'https://www.taobao.com/',
    'https://git-scm.com/',
    'https://www.sohu.com/',
    'https://gitee.com/',
    'https://www.amazon.com/',
    'https://www.usa.gov/',
    'https://www.nasa.gov/'
]


def fetch_page_title(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    content = resp.text
    match = re.compile(r'<title.*?>(.*?)</title>', re.S).search(content)
    print(match.group(1).strip())


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        # map方式
        # pool.map(fetch_page_title, urls)

        # submit方式
        for url in urls:
            pool.submit(fetch_page_title, url)


if __name__ == '__main__':
    main()

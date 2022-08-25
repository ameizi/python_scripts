import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests
from lxml import etree
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

base_url = 'https://s.weibo.com/top/summary?cate=realtimehot'

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

cookies = {
    'SUB': '_2A25MysX2DeRhGedO7loZ9CzFzDmIHXVvobA-rDV8PUNbmtB-LVqskW9NXU6ZHzPAAid8XPEIeIYICjMy1AvT2Pu4',
}


def get_url():
    resp = requests.get(base_url, headers=headers, cookies=cookies)
    html = etree.HTML(resp.text)
    return html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a/@href')


def request_page(page_url):
    if not page_url.startswith('javascript:void(0);'):
        url = urljoin(base_url, page_url)
        resp = requests.get(url, headers=headers)
        logging.info(f'request:{url}')


if __name__ == '__main__':
    url_list = get_url()
    with ThreadPoolExecutor(max_workers=6) as executor:
        list(tqdm(executor.map(request_page, url_list), total=len(url_list)))

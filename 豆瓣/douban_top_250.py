import json
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://movie.douban.com/top250?start=0&filter=',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def fetch(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    for item in soup.find(class_='grid_view').find_all(name='li'):
        index = item.find('em').string
        image = item.find('a').find('img').get('src')
        title = item.find('span', class_='title').string
        rating = item.find('div', class_='star').find('span', class_='rating_num').string
        vote = item.find('div', class_='star').find_all('span')[3].string[:-3]
        if item.find('span', class_='inq'):
            inq = item.find('span', class_='inq').string
        else:
            inq = ''
        dic = dict(index=index, image=image, title=title, rating=rating, vote=vote, inq=inq)
        print(json.dumps(dic, ensure_ascii=False))


if __name__ == '__main__':
    url_list = [f'https://movie.douban.com/top250?start={start * 25}&filter=' for start in range(10)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(fetch, url_list), total=len(url_list)))
    print("done")

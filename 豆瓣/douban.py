import asyncio
import json
import re
import selectors

import aiofiles
import aiohttp
import requests

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://movie.douban.com/top250?start=0&filter=',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

pattern = re.compile(
    r'<li>.*?<em class="">(?P<index>.*?)</em>.*?<img.*?src="(?P<img>.*?)".*?class="title">(?P<title>.*?)</span>'
    r'.*?property="v:average">(?P<rating>.*?)</span>.*?<span>(?P<votes>.*?)人评价</span>'
    r'.*?<span class="inq">(?P<inq>.*?)</span>.*?</li>', re.S)


async def fetch(page):
    start = 25 * page
    url = f'https://movie.douban.com/top250?start={start}&filter='
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            content = await resp.text()
            async with aiofiles.open('douban.txt', 'a', encoding='utf-8') as f:
                for item in re.finditer(pattern, content):
                    await f.write(json.dumps(item.groupdict(), ensure_ascii=False) + '\n')


async def main(loop):
    tasks = []
    for task in (loop.create_task(fetch(index)) for index in range(0, 10)):
        tasks.append(task)
    await asyncio.wait(tasks)
    print("done")


def get():
    for index in range(0, 10):
        start = 25 * index
        url = f'https://movie.douban.com/top250?start={start}&filter='
        resp = requests.get(url, headers=headers)
        for item in re.finditer(pattern, resp.text):
            print(item.groupdict())
    print("done")


if __name__ == '__main__':
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()

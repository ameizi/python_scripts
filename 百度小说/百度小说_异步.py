import asyncio
import json
import os

import aiofiles
import aiohttp
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48"
}


async def aiodownload(book_id, book_name, cid, title):
    if not os.path.exists(book_name):
        os.mkdir(book_name)

    data = {
        "book_id": f"{book_id}",
        "cid": f"{book_id}|{cid}",
        "need_bookinfo": 1
    }
    data = json.dumps(data)
    url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            dic = await resp.json()
            async with aiofiles.open(f"{book_name}/{title}.txt", mode='w', encoding='utf-8') as f:
                await f.write(dic['data']['novel']['content'])


async def getCatalog(book_id, book_name):
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    dic = resp.json()
    tasks = []
    for item in dic['data']['novel']['items']:
        title = item['title']
        cid = item['cid']
        tasks.append(asyncio.create_task(aiodownload(book_id, book_name, cid, title)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(getCatalog('4306063500', '西游记'))
    asyncio.run(getCatalog('4306340013', '儒林外史'))
    asyncio.run(getCatalog('4306339995', '封神演义'))
    asyncio.run(getCatalog('4306340004', '红楼梦'))

import asyncio
import re

import aiohttp

headers = {
    'authority': 'www.gushiji.cc',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'referer': 'https://www.gushiji.cc/mingju/p280.html',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_d_id=b7f7d897f9efefcc9b6bebd6ec85b9; BAIDU_SSP_lcr=https://www.baidu.com/link?url=1likD70OFyfzmt-bukg7V-vdvGsah-sjtz76QDdze5xfw8Vgq3xJsS7hvpPu58wA&wd=&eqid=ab876f29000163900000000461c977b9; n149=149',
}


async def aiodownload(num):
    url = f'https://www.gushiji.cc/mingju/p{num}.html'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            pattern = re.compile(
                r'<li>.*?>(?P<poetry>.*?)</a>.*?class="author">(?P<author>.*?)</a>.*?">(?P<title>.*?)</a>》</li>', re.S)
            content = await resp.text(encoding='utf-8')
            with open('gushiji.csv', 'a', encoding='utf-8') as f:
                for item in pattern.finditer(content):
                    title = item.group('title')
                    author = item.group('author')
                    poetry = item.group('poetry')
                    f.write(",".join([title, author, poetry]) + '\n')


async def main():
    tasks = []
    for i in range(1, 291):
        tasks.append(asyncio.create_task(aiodownload(i)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

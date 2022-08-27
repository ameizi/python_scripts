import asyncio
import re

import aiohttp
from aiohttp import ClientSession

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

TITLE_PATTERN = re.compile(r'<title.*?>(.*?)</title>', re.DOTALL)


async def fetch_page_title(url):
    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36',
    }) as session:  # type: ClientSession
        async with session.get(url, ssl=False) as resp:
            if resp.status == 200:
                html_code = await resp.text()
                matcher = TITLE_PATTERN.search(html_code)
                title = matcher.group(1).strip()
                print(title)


def main():
    objs = [fetch_page_title(url) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(objs))
    loop.close()


if __name__ == '__main__':
    main()

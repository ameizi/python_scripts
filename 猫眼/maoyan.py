import re
import time

import requests

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def get_one_page(url):
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            return resp.text
        return None
    except requests.RequestException:
        return None


def write_to_csv(content):
    with open('maoyan.csv', 'a', encoding='utf-8') as f:
        f.write(content + '\n')


def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?class="board-index.*?">(?P<index>.*?)</i>'
                         r'.*?data-src="(?P<image>.*?)".*?class="name".*?">(?P<title>.*?)</a></p>'
                         r'.*?class="star">(?P<actor>.*?)</p>'
                         r'.*?"releasetime">(?P<rtime>.*?)</p>'
                         r'.*?class="integer">(?P<score>.*?)</i>.*?"fraction">(?P<fraction>.*?)</i>.*?</dd>',
                         re.S)
    for item in re.finditer(pattern, html):
        index = item.group('index')
        image = item.group('image')
        title = item.group('title')
        actor = item.group('actor').strip()[3:]
        rtime = item.group('rtime')[5:]
        score = item.group('score') + item.group('fraction')
        # dic = dict(index=index, image=image, title=title, actor=actor, time=time, score=score)
        write_to_csv(",".join([index, image, title, actor, rtime, score]))


if __name__ == '__main__':
    for offset in range(0, 10):
        print(f"正在抓取{offset + 1}页")
        url = f'https://www.maoyan.com/board/4?offset={offset * 10}'
        html = get_one_page(url)
        parse_one_page(html)
        time.sleep(2)
    print('done')

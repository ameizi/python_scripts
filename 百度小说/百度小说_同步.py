import json
import time

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48"
}


def getCatalog(book_id):
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    dic = resp.json()
    for item in dic['data']['novel']['items']:
        title = item['title']
        cid = item['cid']
        download(book_id, cid, title)


def download(book_id, cid, title):
    data = {
        "book_id": f"{book_id}",
        "cid": f"{book_id}|{cid}",
        "need_bookinfo": 1
    }
    data = json.dumps(data)
    url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"
    resp = requests.get(url, headers=headers)
    dic = resp.json()
    with open(title, mode='w', encoding='utf-8') as f:
        f.write(dic['data']['novel']['content'])
    time.sleep(3)


if __name__ == '__main__':
    getCatalog('4306063500')

import logging
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.89 Safari/537.36"
}
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def save(index, url):
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    with open(f'{index}.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)


if __name__ == '__main__':
    resp = requests.get("https://www.liaoxuefeng.com/wiki/1252599548343744", headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    urls = []
    for a in menu_tag.find_all("a"):
        urls.append(f"https://www.liaoxuefeng.com{a.get('href')}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda args: save(*args), [(index, url) for index, url in enumerate(urls)])

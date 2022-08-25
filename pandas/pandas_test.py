import time

import pandas as pd
import requests
import urllib3

urllib3.disable_warnings()


def example1():
    url = 'http://www.compassedu.hk/qs'
    df = pd.read_html(url)[0].iloc[::, :-1]  # 0表示网页中的第一个Table
    df.to_csv('世界大学综合排名.csv', mode='w', index=False)


def example2():
    df = pd.DataFrame()
    for i in range(6):
        page = i + 1
        url = f'http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jjzc/index.phtml?p={page}'
        df = pd.concat([df, pd.read_html(url)[0].iloc[::, :-1]])
        print(f'第{page}页抓取完成')
    df.to_csv('新浪财经数据.csv', mode='w', encoding='utf-8', index=False)


def example3():
    start = time.time()
    df = pd.DataFrame(data=None, columns=['公司名称', '披露类型', '上市板块', '保荐机构', '披露时间', '公告'])
    for page in range(1, 51):
        url = f'http://eid.csrc.gov.cn/ipo/1010/index_{page}.html'
        df = pd.concat([df, pd.read_html(url)[0]])
        print(f'第{page}页抓取完成')

    df.to_csv('沪市IPO公司.csv', encoding='utf-8', index=False)  # 保存数据到csv文件
    end = time.time()
    print('共抓取', len(df), '家公司,' + '用时', round((end - start) / 60, 2), '分钟')


def example4():
    start = time.time()
    df = pd.DataFrame(data=None, columns=['品名', '属性参数', '最新报价', '单位', '报价数', '报价时间'])
    for page in range(1, 597):
        url = f'https://www.zhongnongwang.com/quote/product-htm-page-{page}.html'
        resp = requests.get(url, verify=False)
        resp.encoding = 'utf-8'
        df = pd.concat([df, pd.read_html(resp.text)[0]])
        print(f'第{page}页抓取完成')

    df.to_csv('产品报价.csv', encoding='utf-8', index=False)  # 保存数据到csv文件
    end = time.time()
    print('共抓取', len(df), '个产品报价,' + '用时', round((end - start) / 60, 2), '分钟')


def weibo():
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
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    resp = requests.get(url, headers=headers, cookies=cookies)
    df = pd.read_html(resp.text, encoding='utf-8', skiprows=1)[0]  # 跳过第一行，查找页面中第一个表格
    df.columns = ['index', 'title', 'tag']  # 重命名列名
    df = df[df['index'] != '•']  # 过滤掉index不为'•'的行数据
    df = df.iloc[:, :-1]  # '取所有行数据，不包含最后一列 tag'
    df['news'] = df['title'].apply(lambda x: x.split('  ')[0])  # 拆分列
    df['hot'] = df['title'].apply(lambda x: x.split('  ')[1])  # 拆分列，并新增一列
    df.drop(axis=1, labels='title', inplace=True)  # 删除列
    df.to_csv('weibo.csv', mode='w', encoding='utf-8', index=False, sep=',')
    print('done')


if __name__ == '__main__':
    # example1()
    # example2()
    # example3()
    # example4()
    weibo()

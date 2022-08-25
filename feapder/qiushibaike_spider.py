import json

import feapder


class QiushibaikeSpider(feapder.AirSpider):

    def start_requests(self):
        for i in range(1, 15):
            yield feapder.Request(f"https://www.qiushibaike.com/8hr/page/{i}/")

    def parse(self, request, response):
        article_list = response.xpath('//a[@class="recmd-content"]')
        for article in article_list:
            title = article.xpath("./text()").extract_first()
            url = article.xpath("./@href").extract_first()

            yield feapder.Request(
                url, callback=self.parse_detail, title=title
            )  # callback 为回调函数

    def parse_detail(self, request, response):
        """
        解析详情
        """
        response.encoding_errors = "ignore"
        # 取url
        url = request.url
        # 取title
        title = request.title
        # 解析正文
        content = response.xpath(
            'string(//div[@class="content"])'
        ).extract_first()  # string 表达式是取某个标签下的文本，包括子标签文本
        dic = dict(title=title, content=content, url=url)
        print(json.dumps(dic, ensure_ascii=False))


if __name__ == "__main__":
    QiushibaikeSpider(thread_count=50).start()

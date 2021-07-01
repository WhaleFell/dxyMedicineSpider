'''
Author: whalefall
Date: 2021-06-20 10:21:21
LastEditTime: 2021-07-01 17:51:15
Description: 爬取丁香园用药助手 关于抑郁症的所有用药数据
'''
import requests
from urllib import parse
from lxml import etree
import json


class Depression(object):

    def __init__(self) -> None:

        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
            # "":"Referer: http://drugs.dxy.cn/search/indication?keyword=%E6%8A%91%E9%83%81%E7%97%87&page=7"
        }

        self.se = requests.session()

        # 导出md格式
        # self.markdown_table_header = """| 药物名称(俗名) | 主要成分 | 主治 | 药品公司 |\n| :--: |----| ---- | ---- |\n"""
        # self.markdown_table_row = """| %s | %s | %s | %s |\n"""
        self.markdown_table_header = """| 药物名称(俗名) | 主治 |\n| :--: |----|\n"""
        self.markdown_table_row = """| %s | %s |\n"""

    def getIndex(self, page) -> dict:
        url = "http://drugs.dxy.cn/search/indication?keyword=%s&page=%s" % (
            parse.quote("抑郁症"), page)

        try:
            resp = self.se.get(url, headers=self.header)
            html = etree.HTML(resp.text)
            resultRaw = html.xpath("/html/body/script[3]/text()")[0]
            resultJson = json.loads(resultRaw)
            return resultJson['props']['pageProps']["result"]
        except Exception as e:
            print("第%s页解析失败" % (page))
            return None

    def writeMD(self, resultJson):
        if resultJson == None:
            return None
        for one in resultJson:
            name = "%s(%s)" % (one['commonName'], one['cnName'])
            component = one['component']
            indication = one["indication"]
            companyName = one['companyName']
            # print(name, component, indication, companyName)
            with open("medicineSimple.md", "a", encoding="utf8") as md:
                md.write(self.markdown_table_row %
                         (name, indication))
                         
        print("写入成功")

    def main(self):
        with open("medicineSimple.md", "w", encoding="utf8") as md:
            md.write(self.markdown_table_header)
            
        for i in range(0, 24):
            resultJson = self.getIndex(i)
            self.writeMD(resultJson)


if __name__ == "__main__":
    # Depression().getIndex(2)
    Depression().main()

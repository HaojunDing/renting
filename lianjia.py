import requests as r
from lxml import etree
from Mysql_req import Mysql_conn

m = Mysql_conn()
sql = 'INSERT INTO lianjiainfo (title, region, zone, meters, con, img_url, link, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
base_url = 'https://bj.lianjia.com/zufang/daxing/pg{}/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

page = int(input('请输入要爬取得页数:'))

for i in range(1, page+1):
    url = base_url.format(str(i))
    html_byte = r.get(url, headers=headers)
    html_element = etree.HTML(html_byte.text)
    # 通过xpath匹配到ul下的li
    ul_list = html_element.xpath('//ul[@id="house-lst"]/li')
    for li_element in ul_list:
        title = li_element.xpath('./div[2]/h2/a')[0].text
        region = li_element.xpath('./div[2]/div[1]/div[1]/a/span')[0].text
        zone = li_element.xpath('./div[2]/div[1]/div[1]/span[1]/span')[0].text
        meters = li_element.xpath('./div[2]/div[1]/div[1]/span[2]')[0].text
        con = li_element.xpath('./div[2]/div[1]/div[2]/div/a')[0].text
        link1 = li_element.xpath('./div[1]/a/@href')[0]
        link = repr(link1)
        img_url1 = li_element.xpath('./div[1]/a/img/@data-img')[0]
        img_url = repr(img_url1)
        price = li_element.xpath('./div[2]/div[2]/div[1]/span')[0].text
        data = title, region, zone, meters, con, img_url, link, price
        print(title, region, zone, meters, con, img_url, link, price)
        m.ins(sql, data)
        # break


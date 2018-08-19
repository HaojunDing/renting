import requests as r
from lxml import etree
from Mysql_req import Mysql_conn
from urllib import parse



def woaiwojia (page):
    m = Mysql_conn()

    base_url = 'https://bj.5i5j.com/zufang/n{}/'
    sql = 'INSERT INTO woaowojiainfo (tltle, hall, area, fit, site, site_ditie,  link, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'


    # page = int(input('请输入爬取页数'))

    headers = {
        'Host': 'bj.5i5j.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Cookie': '_Jo0OQK=76A477F3AE6EA92F43235C9451A72C718926BC1A7F597AAAF865F7D8EA67390A3248EA151B6F8F92C5007A098490BF7CBAAA36181EC9F8FCFD4071DE5F66C6B5E1FC57212F12283777C840763663251ADEB840763663251ADEB7FADEAD9F99B65226ECAC92C8E815B0AGJ1Z1ZA=='
    }

    for i in range(1, page+1):
        url = base_url.format(i)
        print(url)
        html = r.get(url, headers=headers).text
        # print(html)

        html_ele = etree.HTML(html)
        li_list = html_ele.xpath('//ul[@class="pList"]/li')
        # print(li_list)
        for li_ele in li_list:
            tltle = li_ele.xpath('./div[2]/h3/a')[0].text
            # print(tltle)
            info = li_ele.xpath('./div[2]/div[1]/p[1]/text()')[0].split('·')
            hall = info[0].replace(' ', '')
            area = info[1].replace(' ', '')
            fit = info[-1].replace(' ', '')
            site = li_ele.xpath('./div[2]/div[1]/p[2]/a')[0].text
            if li_ele.xpath('./div[2]/div[1]/p[2]/text()') != []:
                site_ditie = li_ele.xpath('./div[2]/div[1]/p[2]/text()')[0].replace(' · ', '')
            else:
                site_ditie = 'None'
            # print(site_ditie,type(site_ditie))
            # img_src = repr(li_ele.xpath('./div[1]/a/img/@src'))
            link_pinjie = li_ele.xpath('./div[2]/h3/a/@href')[0]
            # print(link_pinjie)
            link = repr(parse.urljoin(url, link_pinjie))
            # print(link)
            price = li_ele.xpath('./div[2]/div[1]/div/p[1]/strong')[0].text
            data = tltle, hall, area, fit, site, site_ditie, link, price
            m.ins(sql, data)
    return '已下载完成'


if __name__ == '__main__':
    page = int(input('请输入要爬取页数:'))
    print(woaiwojia(page))
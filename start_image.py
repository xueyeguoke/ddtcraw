# 爬取明星图片   http://www.win4000.com/mt/star_1_0_1.html
# -*-coding:utf8-*-

import requests
import datetime
from lxml import etree
import os


def download():
    # time1 = datetime.datetime.now()

    for i in range(1):
        url = 'http://www.win4000.com/mt/star_1_0_' + str(i + 1) + '.html'
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        target = {
            "//div[@class='list_cont list_cont2 w1180']//div[@class='tab_zt']//div[@class='tab_box']//div//ul[@class='clearfix']//li//a": 'href',
            "//div[@class='list_cont list_cont2 w1180']//div[@class='tab_zt']//div[@class='tab_box']//div//ul[@class='clearfix']//li//a//img": 'alt'
        }
        star_page = get_html(url, head, target)
        for star_url, name in zip(star_page[0], star_page[1]):
            print('{}--{},'.format(name, star_url))

            img_dir = os.path.join('./img/' + name)
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            target = {
                "//div[@class='list_cont Left_list_cont  Left_list_cont2']//div[@class='tab_tj']//div[@class='tab_box']//div//ul[@class='clearfix']//li//a//img": 'src'
            }
            star_images = get_html(star_url, head, target)
            target = {
                "//div[@class='list_cont Left_list_cont  Left_list_cont2']//div[@class='tab_tj']//div[@class='tab_box']//div//ul[@class='clearfix']//li//a//img": 'title'
            }
            img_names = get_html(star_url, head, target)
            for img_url, img_name in zip(star_images[0], img_names[0]):
                imgdata = requests.get(img_url, headers=head)
                with open(os.path.join(img_dir, img_name + '.jpg'), 'wb') as f:
                    f.write(imgdata.content)


def get_html(url, head, targets):
    rst = []
    response = requests.session().get(url, headers=head)
    html = etree.HTML(response.text)
    for target in targets:
        content = html.xpath(target)
        val = html.xpath(target)  # 使用xpath函数，返回文本列表
        rst_tmp = []
        for v in (val):
            rst_tmp.append(v.attrib[targets[target]])
        rst.append(rst_tmp)

    return rst


url = 'http://www.win4000.com/mt/shangyuxian.html'
download()


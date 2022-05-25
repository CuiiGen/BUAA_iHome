# -*- coding: utf-8 -*-
import _thread
import logging
from os import makedirs
from time import localtime, strftime

import requests
from lxml import etree

# 配置logging模块
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - "%(pathname)s", line %(lineno)d - %(funcName)s - %(message)s'
)

# 相对路径
path = strftime('%Y_%m%d_%H_%M%S', localtime())
# 建立文件夹
makedirs(f'{path}/complain_item')
# cookie
cookie = ''


def getDetail(doid):
    '''
    获取问题及回复详情页面
    :doid
    '''
    logging.info(f'详情{doid}查询……')
    # 基本信息
    url = 'http://i.buaa.edu.cn/space.php'
    param = {'do': 'complain_item', 'doid': doid}
    # 请求头
    header = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'i.buaa.edu.cn',
        'Referer': 'http://i.buaa.edu.cn/space.php?do=complain',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    # 请求
    r = requests.get(url, params=param, headers=header)
    r.encoding = 'utf-8'
    # 解析
    h = etree.HTML(r.text)
    # 获取信息
    li = h.xpath('//*[@id="content"]/div[2]/ol/li')
    detail = etree.tostring(li[0], encoding='utf-8', method='html').decode('utf-8')
    # 保存
    with open(f'{path}/complain_item/{doid}.html', 'w', encoding='utf-8') as f:
        f.write(detail)
        f.flush()
    logging.info(f'详情{doid}查询成功')


def main():
    '''
    主函数，获取诉求列表
    '''
    # 基本信息
    url = 'http://i.buaa.edu.cn/space.php'
    param = {'do': 'complain', 'view': 'all', 'type': 'all', 'page': 2}
    form = {'atuid': 0}

    # 请求头
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Host': 'i.buaa.edu.cn',
        'Origin': 'http://i.buaa.edu.cn',
        'Referer': 'http://i.buaa.edu.cn/space.php?do=complain',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    style = '''
    <style>
            table {
                    border-collapse: collapse;
                    margin: 0 auto;
                    text-align: left;
            }

            table th {
                    border: 1px solid #cad9ea;
                    color: #666;
                    height: 30px;
            }

            table thead th {
                    background-color: #CCE8EB;
                    width: 100px;
            }

            table tr:nth-child(odd) {
                    background: #fff;
            }

            table tr:nth-child(even) {
                    background: #F5FAFA;
            }

            a:link {
                    color: cornflowerblue;
            }

            a:visited {
                    color: darkolivegreen;
            }
    </style>
    '''
    with open(f'{path}/index.html', 'a', encoding='utf-8') as f:
        f.write(style)
        f.flush()

    # 页码循环
    page = 1
    while True:
        # 更新QueryParameters
        param['page'] = page
        logging.info(f'获取页面{page}的信息')
        # 获取请求
        r = requests.post(url, params=param, data=form, headers=header)
        r.encoding = 'utf-8'
        # 解析
        h = etree.HTML(r.text)
        # 获取href
        href = h.xpath('//div[@class="complain_list_container"]/table[@class="complain_list"]/tbody/tr/td[1]/a')
        # 检查是否空页面
        if len(href) == 0:
            break
        # 修改href
        for i in href:
            j = i.attrib.get('href')[32:]
            _thread.start_new_thread(getDetail, (j, ))
            # getDetail(j)
            i.set('href', f'complain_item/{j}.html')
        # 获取列表
        complain_list = h.xpath('//div[@class="complain_list_container"]/table[@class="complain_list"]')
        complain_list[0].set('cellpadding', '15')
        # 获取outerhtml
        table = etree.tostring(complain_list[0], encoding='utf-8',method='html').decode('utf-8')
        # 保存结果
        with open(f'{path}/index.html', 'a', encoding='utf-8') as f:
            f.write(table)
            f.flush()
        # 下一页
        page += 1


if __name__ == '__main__':
    main()

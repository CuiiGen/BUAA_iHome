# -*- coding: utf-8 -*-
import logging
from time import localtime, strftime, time

import requests
from lxml import etree

# 配置logging模块
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - "%(pathname)s", line %(lineno)d - %(funcName)s - %(message)s'
)

# 相对路径
path = strftime('%Y_%m%d_%H_%M%S', localtime())


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
        'Cookie':
        'ihome_sendmail=1; ihome_loginuser=ZY2003503; ihome_seccode=e477uSo/C8Av2V/JQ/+BDdfw8CFs1GxDG+8LWC/Xdf8g; ihome_auth=8e61vWCQqJj/09aiFDBzPj2oGOkuvMM0ehshR95/rHXPbgBoVUJK37R3fnGhXtDUukWv63AvtMyItLMCFazbQHQFhg; ihome_checkpm=1',
        'Host': 'i.buaa.edu.cn',
        'Origin': 'http://i.buaa.edu.cn',
        'Referer': 'http://i.buaa.edu.cn/space.php?do=complain',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

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
            j = i.attrib.get('href')
            print(j)
            i.set('href', f'complain_item/{j[32:]}.html')
        # 获取列表
        complain_list = h.xpath('//div[@class="complain_list_container"]/table[@class="complain_list"]')
        # 获取outerhtml
        table = etree.tostring(complain_list[0], encoding='utf-8').decode('utf-8')
        # 保存结果
        with open(f'{path}/a.html', 'a', encoding='utf-8') as f:
            f.write(table)
            f.flush()
        # 下一页
        page += 1


if __name__ == '__main__':
    main()

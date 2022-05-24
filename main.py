# -*- coding: utf-8 -*-
import requests
from lxml import etree


def main():
    url = 'http://i.buaa.edu.cn/space.php'
    param = {'do': 'complain', 'view': 'all', 'type': 'all', 'page': 2}
    form = {'atuid': 0}

    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':
        'ihome_loginuser=ZY2003503; UM_distinctid=18068e837dd141-00f2d0e465691d-6b3e555b-384000-18068e837dec87; Hm_lvt_8edeba7d3ae859d72148a873531e0fa5=1653295087,1653299629,1653305417,1653306778; Hm_lpvt_8edeba7d3ae859d72148a873531e0fa5=1653306778; ihome_seccode=b203KDrJ36UkYUIbuQjQm0r69GpzpuPyReHi86g4gHmL; ihome_auth=1b4ce2kWCim6wZ2GVnhkYAEe8AGLk1W6EQCTnuoerx2Ld7%2B%2FTmFFfg63%2FojHBvprB5hF80Ku%2F6Rv9Fo7%2BzDFRjGb3g; ihome_sendmail=1; ihome_checkpm=1',
        'Host': 'i.buaa.edu.cn',
        'Origin': 'http://i.buaa.edu.cn',
        'Referer': 'http://i.buaa.edu.cn/space.php?do=complain',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    r = requests.post(url, params=param, data=form, headers=header)
    r.encoding = 'utf-8'
    h = etree.HTML(r.text)
    href = h.xpath(
        '//div[@class="complain_list_container"]/table[@class="complain_list"]/tbody/tr/td[@class="info_tip "]/a'
    )
    for i in href:
        j = i.attrib.get('href')
        print(j)
        i.set('href', f'complain_item/{j[32:]}.html')
    complain_list = h.xpath(
        '//div[@class="complain_list_container"]/table[@class="complain_list"]')
    table = etree.tostring(complain_list[0], encoding='utf-8').decode('utf-8')
    with open('a.html', 'w', encoding='utf-8') as f:
        f.write(table)
        f.flush()


if __name__ == '__main__':
    main()

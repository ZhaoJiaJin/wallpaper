#!/usr/bin/env python

import os
import requests
import re
import urllib


"""
下载策略：
1，初始化时下载第一页的壁纸，并记录
2，每次更新壁纸检查第一页的第一张有没有更新，如果有，下载并更换
3，需要记录第一张壁纸的名称，需要记录最后一张壁纸的页码和位置
4，如果没有更新的话，从记录的最后一张壁纸开始下载，


"""


page = 0
base = "http://wallpaperswide.com"
url = '{1}/top_wallpapers/page/{0}'.format(page,base)
resolution = ['1920x1080','2048x1152','2400x1350','2560x1440','2880x1620','3554x1999']


first = ""
pic_idx = 1


def download_pic(link):
    pic_name = "wallpaper/" + link.split('/')[-1]
    urllib.request.urlretrieve('{0}{1}'.format(base,link),pic_name)
    return pic_name


def parse_rec(data):
    herf = data.split()[0]
    url = herf.split('=')[1].strip('"')
    return url


def get_pic(pic_page_url):
    full_url = '{0}{1}'.format(base,pic_page_url)
    pic_html = requests.get(full_url)
    html = pic_html.text
    for resu in resolution:
        pat = re.compile(r'<a target="_self".*{0}</a>'.format(resu))
        pic_url = pat.findall(html)
        for p in pic_url:
            return p.split()[2].split('=')[1].strip('"')




data = requests.get(url)

pa = re.compile(r'href=".*wallpapers.html".*itemprop="significantLinks"')
res = pa.findall(data.text)
for rec in res:
    pic_page_url = parse_rec(rec)
    pic_link = get_pic(pic_page_url)
    pic_name = download_pic(pic_link)



#os.system("feh --randomize --bg-fill /home/jin/Pictures/*.jpg")

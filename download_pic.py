#!/usr/bin/env python

import os
import requests
import re
import urllib
import time

"""
下载策略：
1，初始化时下载第一页的壁纸，并记录
2，每次更新壁纸检查第一页的第一张有没有更新，如果有，下载并更换
3，需要记录第一张壁纸的名称，需要记录最后一张壁纸的页码和位置
4，如果没有更新的话，从记录的最后一张壁纸开始下载，


"""


#page = 0
base = "http://wallpaperswide.com"
#url = '{1}/top_wallpapers/page/{0}'.format(page,base)
resolution = ['1920x1080','2048x1152','2400x1350','2560x1440','2880x1620','3554x1999']
interval = 300


first_link = ""
page_idx = 0
pic_idx = 1


def save_stat():
    with open('.pic_status','w') as f:
        f.write('{0}\t{1}\t{2}'.format(page_idx,pic_idx,first_link))

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



def init():
    with open('.pic_status','r') as f:
        content = f.read()
        f_s = content.split('\t')
        page_idx = f_s[0]
        pic_idx = f_s[1]
        first_link = f_s[2]





def get_first():
    url = '{0}/top_wallpapers/page/0'.format(base)
    data = requests.get(url)

    pa = re.compile(r'href=".*wallpapers.html".*itemprop="significantLinks"')
    res = pa.findall(data.text)
    rec = res[0]
    pic_page_url = parse_rec(rec)
    pic_link = get_pic(pic_page_url)
    return pic_link



def get_cur_pic_link():
    url = '{0}/top_wallpapers/page/{1}'.format(base,page_idx)
    data = requests.get(url)

    pa = re.compile(r'href=".*wallpapers.html".*itemprop="significantLinks"')
    res = pa.findall(data.text)
    try:
        rec = res[pic_idx]
    except Exception as e:
        page_idx += 1
        pic_idx -= len(rec)
        save_stat()
        url = '{0}/top_wallpapers/page/{1}'.format(base,page_idx)
        data = requests.get(url)

        pa = re.compile(r'href=".*wallpapers.html".*itemprop="significantLinks"')
        res = pa.findall(data.text)
        rec = res[pic_idx]
    pic_page_url = parse_rec(rec)
    pic_link = get_pic(pic_page_url)
    return pic_link




def update_wallpaper():
    new_first = get_first()
    if new_first != first_link:
        new_wallpaper = download_pic(new_first)
        first_link = new_first
        save_stat()
    else:
        cur_link = get_cur_pic_link()
        pic_name = "wallpaper/" + link.split('/')[-1]
        while os.path.isfile(pic_name):
            print("pic already exist, find next pic "+pic_name)
            pic_idx += 1
            save_stat()
            cur_link = get_cur_pic_link()
            pic_name = "wallpaper/" + link.split('/')[-1]
        new_wallpaper = download_pic(cur_link)

    os.system("feh --randomize --bg-fill {0}".format(new_wallpaper))





try:
    init()
except Exception as e:
    page_idx = 0
    pic_idx = 0
    first_link = ""


while(True):
    update_wallpaper()
    time.sleep(interval)



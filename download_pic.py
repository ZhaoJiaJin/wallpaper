#!/usr/bin/env python

import os
import requests
import re

page = 0
base = "http://wallpaperswide.com"
url = '{1}/top_wallpapers/page/{0}'.format(page,base)
resolution = ['1920x1080','2048x1152','2400x1350','2560x1440','2880x1620','3554x1999']




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
    print (pic_link)



#os.system("feh --randomize --bg-fill /home/jin/Pictures/*.jpg")

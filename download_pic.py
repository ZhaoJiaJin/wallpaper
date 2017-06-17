#!/usr/bin/env python

import os
import requests
import re

page = 0
url='http://wallpaperswide.com/top_wallpapers/page/{0}'.format(page)




def parse_rec(data):
    herf = data.split()[0]
    url = herf.split('=')[1].strip('"')
    print (url)




data = requests.get(url)

pa = re.compile(r'href=".*wallpapers.html".*itemprop="significantLinks"')
res = pa.findall(data.text)
for rec in res:
    parse_pic(rec)



#os.system("feh --randomize --bg-fill /home/jin/Pictures/*.jpg")

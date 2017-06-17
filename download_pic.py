#!/usr/bin/env python

import os
import requests

page = 0
url='http://wallpaperswide.com/top_wallpapers/page/{0}'.format(page)


data = requests.get(url)
print (data.text)




#os.system("feh --randomize --bg-fill /home/jin/Pictures/*.jpg")

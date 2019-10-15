import requests
import ftplib

from PIL import Image
import glob
import time
import os
import sys

# Install imageMagick
# > sudo apt-get install imagemagick

while True:
    url = 'http://altair12.net/imatges/webcam/exterior01/petita.jpg'
    search_dir = "../resources/"

    files_sort_by_name = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
    files_sort_by_name.sort()
    files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))

    files.sort(key=lambda x: os.path.getmtime(x))

    # download Image
    # -------------------------------------------------------------------
    if len(files) < 10:
        filename = "../resources/0{}.jpg".format(len(files))
    elif len(files) < 50:
        filename = "../resources/{}.jpg".format(len(files))
    else:
        filename = files[0]

    r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Chrome'})
    open(filename, 'wb').write(r.content)

    # Create animated Gif
    # -------------------------------------------------------------------
    dataDir = '../resources/'
    os.chdir(dataDir)
    os.system('convert *.jpg ../loop.gif')
    os.chdir('../')

    # Upload with ftp
    # -------------------------------------------------------------------
    # upload to FTP
    session = ftplib.FTP(os.environ['URL'], os.environ['USERNAME'], os.environ['PASSWORD'])
    file = open('loop.gif', 'rb')
    session.storbinary('STOR loop.gif', file)
    file.close()
    session.quit()

    time.sleep(300)

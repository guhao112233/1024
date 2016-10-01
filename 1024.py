#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
import urllib
import urllib2
from PIL import Image
from StringIO import StringIO

picUrl = "http://cl.vgtr.biz/thread0806.php?fid=16"
basePicUrl = "http://cl.vgtr.biz/"
fileName = "/workspace/py_work/file"
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; CrOS x86_64 6253.0.0) AppleWebKit/537.36 " \
    "(KHTML, like Gecko) Chrome/39.0.2151.4 Safari/537.36"
}




def searchPicPage():
    count =0
    session = requests.session()
    session.headers.update(headers)
    r = session.get(picUrl)
    r.encoding = "gbk"
    html = r.text

    soup = BeautifulSoup(html)
    divs = soup.find_all("div", class_="t")
    soupdiv = BeautifulSoup(str(divs[1]))
    for a in soupdiv.find_all("a", target="_blank", href = re.compile("htm_data"), title=""):
        soupa = BeautifulSoup(str(a))
        attrs = soupa.a.attrs
        thisPicUrl = basePicUrl + attrs["href"]
        print(thisPicUrl)
        searchPicDown(thisPicUrl, session)
        count +=1
        if count >=100:
            break


def searchPicDown(url, session):

    r= session.get(url)
    r.encoding = "gbk"
    soup = BeautifulSoup(r.text)
    for img in soup.find_all("input", type="image"):
        image = BeautifulSoup(str(img))
        image_url = image.input.attrs["src"]
        # print(image_url)
        try:
            response = session.get(image_url, stream=True, timeout=2)
        except:
            pass
        # response.
        # r_image = response.content
        print(image_url)
        suffix = image_url.split('.')[-1]
        filename = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + str(datetime.datetime.now().microsecond) + "."+suffix
        print(filename)
        try:
            urllib.urlretrieve(image_url,createFileWithFileName(fileName, filename))
        except:
            pass


def createFileWithFileName(localPathParam, fileName):
    totalPath = localPathParam+os.sep + fileName
    if not os.path.exists(totalPath):
        file = open(totalPath, 'a+')
        file.close()
        return totalPath

if __name__ == '__main__':
    print("1:文章")
    print("2:图片")
    print("3:视频")
    choose = input("请输入代号:")
    if choose == 1:
        pass
    elif choose == 2:
        searchPicPage()
        print("下载完成")
    elif choose == 3:
        pass
    else:
        print("请正确输入代号")

#-*-coding:utf8-*-
 
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
if(len(sys.argv)>=2):
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"请输入user_id: "))
cookie = {"Cookie": "SCF=AhmdDLBJaBVBeFi-lFjLjjj6NI6OuQwADIRZbZfP7WPpEXVcpoB0l8fjYbuwRnYKeR2oRb4Kg9Kil2SF_Nl7uLc.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWwTAhFF1bWvP3x5YS0MM0v5JpX5o2p5NHD95Q0eKq7SK.c1h-0Ws4Dqcj.i--fi-z7iKnpi--Xi-iWiKy8i--ciKLhi-i2i--ciKLhi-2R; _T_WM=48da1533b7a1bf8010e449af9704301e; WEIBOCN_FROM=home; M_WEIBOCN_PARAMS=luicode%3D20000173; SUB=_2A251AxRwDeTxGeVP7VIU-SjEzj-IHXVWD7w4rDV6PUJbkdBeLUbRkW0-ia4mGQbG7FMpDtWxK6pIULsMAA..; SUHB=02M_TOAeXIZZlE; SSOLoginState=1476879392"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id
html = requests.get(url, cookies = cookie).content
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])    
result = "" 
urllist_set = set()
word_count = 1
image_count = 1
 
print u'爬虫准备就绪...'
 
for page in range(1,pageNum+1):
 
  #获取lxml页面
  url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
  lxml = requests.get(url, cookies = cookie).content
 
  #文字爬取
  selector = etree.HTML(lxml)
  content_txt = selector.xpath('//span[@class="ctt"]')
  
  for each_1 in content_txt:
    text = each_1.xpath('string(.)')
    
    if word_count >= 4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1
 
  #图片爬取
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  for imgurl in urllist:
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    image_count +=1
 
fo = open("/home/gzd/python/weibo/%s"%user_id, "wb")
fo.write(result)
word_path=os.getcwd()+'/%d'%user_id
print u'文字微博爬取完毕'
 
link = ""
fo2 = open("/home/gzd/python/weibo/%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
  link = link + eachlink +"\n"
fo2.write(link)
print u'图片链接爬取完毕'
 
if not urllist_set:
  print u'该页面中不存在图片'
else:
  #下载图片,保存在当前目录的pythonimg文件夹下
  image_path=os.getcwd()+'/weibo_image'
  if os.path.exists(image_path) is False:
    os.mkdir(image_path)
  x=1
  for imgurl in urllist_set:
    temp= image_path + '/%s.jpg' % x
    print u'正在下载第%s张图片' % x
    try:
      urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
    except:
      print u"该图片下载失败:%s"%imgurl
    x+=1
 
print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)

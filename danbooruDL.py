
# coding: utf-8

# In[3]:


#coding=utf-8
import urllib.request as request
import xml
from bs4 import BeautifulSoup
import os
import urllib

def urllib_download(pic_url, file_path):
    from urllib.request import urlretrieve
    urlretrieve(pic_url, file_path)

def get_pic_url(soup):
    pic_url=[]
    for i in soup.find_all('article'):
        pic=i.find_all('a')
        pic=pic[0]['href']
        pic='https://danbooru.donmai.us'+pic
        pic_url.append(pic)
    return pic_url

def get_one_page(url):
    global opener
    origin_bytes = opener.open( url ).read()
    origin_string = origin_bytes.decode( 'utf-8' )
    soup = BeautifulSoup(origin_string, "lxml")
    return soup

def get_picinfo(soup):
    info=soup.find_all('section',id='post-information')
    info=info[0].find_all('li')
    id_info=info[0].string.strip('<li>ID: ').strip('</li>')
    try:
        wsize_info=soup.find_all('span',itemprop="width")
        wsize_info=wsize_info[0].string
        hsize_info=soup.find_all('span',itemprop="height")
        hsize_info=hsize_info[0].string
        size_info=wsize_info+'x'+hsize_info
    except:
        size_info='0x0'
    info=[id_info,size_info]
    return info


def get_pic_ori(soup,file_path,pic_info):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    pic=soup.find_all('section',id='image-container')
    pic=pic[0]['data-file-url']
    print ("Downloading Original Picture...ID="+pic_info[0]+" SIZE="+pic_info[1])
    request = urllib.request.Request(pic, None, headers)  
    response = urllib.request.urlopen(request)
    with open(file_path+pic_info[0]+'.png', "wb") as f:
        f.write(response.read())
    print ("OK...ID="+pic_info[0])
    return
    
def get_pic_larger(soup,file_path,pic_info):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    pic=soup.find_all('section',id='image-container')
    pic=pic[0]['data-large-file-url']
    print ("Downloading Larger Picture...ID="+pic_info[0]+" SIZE="+pic_info[1])
    request = urllib.request.Request(pic, None, headers)  
    response = urllib.request.urlopen(request)
    with open(file_path+pic_info[0]+'.jpg', "wb") as f:
        f.write(response.read())
    print ("OK...ID="+pic_info[0])
    return
    
def main():
    url = 'https://danbooru.donmai.us/posts?tags=himeno_sena'
    file_path='./image/'
    os.makedirs(file_path, exist_ok=True)
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    global opener
    opener = request.build_opener()
    opener.addheaders = [ headers ]
    for n in range(1,3):
        url='https://danbooru.donmai.us/posts?page='+str(n)+'&tags=himeno_sena'
        soup=get_one_page(url)
        pic_url=get_pic_url(soup)
        for i in pic_url:
            soup=get_one_page(i)
            pic_info=get_picinfo(soup)
            try:
                get_pic_ori(soup,file_path,pic_info)
            except:
                get_pic_larger(soup,file_path,pic_info)
    print ('Program Over.')
    
main()


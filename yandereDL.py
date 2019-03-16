
# coding: utf-8

# In[1]:


#coding=utf-8
import urllib.request as request
import xml
from bs4 import BeautifulSoup
import os


def urllib_download(pic_url, file_path):
    from urllib.request import urlretrieve
    urlretrieve(pic_url, file_path)

def get_pic_url(soup):
    pic_url=[]
    for i in soup.find_all('a',class_='thumb'):
        pic=i.find_all('span')
        pic=pic[0].string.strip('#pl ')
        pic_url.append(pic)
    return pic_url

def get_one_page(url):
    global opener
    origin_bytes = opener.open( url ).read()
    origin_string = origin_bytes.decode( 'utf-8' )
    soup = BeautifulSoup(origin_string, "lxml")
    return soup

def get_picinfo(soup):
    info=soup.find_all('div',id='stats')
    info=info[0].find_all('li')
    id_info=info[0].string.strip('<li>Id: ').strip('</li>')
    size_info=info[2].string.strip('<li>Size: ').strip('</li>')
    info=[id_info,size_info]
    return info

def get_pic_ori(soup,file_path,pic_info):
    pic=soup.find_all('a',class_='original-file-unchanged')
    pic=pic[0]['href']
    print ("Downloading Original Picture...ID="+pic_info[0]+" SIZE="+pic_info[1])
    urllib_download(pic,file_path+pic_info[0]+'.png')
    print ("OK...ID="+pic_info[0])
    return
    
def get_pic_larger(soup,file_path,pic_info):
    pic=soup.find_all('a',class_='original-file-changed')
    pic=pic[0]['href']
    print ("Downloading Larger Picture...ID="+pic_info[0]+" SIZE="+pic_info[1])
    urllib_download(pic,file_path+pic_info[0]+'.png')
    print ("OK...ID="+pic_info[0])
    return
    
def main():
    url = 'https://yande.re/post?tags=dakimakura'
    file_path='./image/'
    os.makedirs(file_path, exist_ok=True)
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    global opener
    opener = request.build_opener()
    opener.addheaders = [ headers ]
    for n in range(1,8):
        #url='https://yande.re/post?page='+str(n)+'&tags=dakimakura'
        url='https://yande.re/post?page='+str(n)+'&tags=himeno_sena'
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


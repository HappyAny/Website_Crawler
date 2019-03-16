
# coding: utf-8

# In[88]:


#coding=utf-8
import urllib.request as request
import xml,time
from bs4 import BeautifulSoup
import os
import urllib
import requests
import http.cookiejar as cj

def urllib_download(pic_url, file_path):
    from urllib.request import urlretrieve
    urlretrieve(pic_url, file_path)

def get_pool_url(soup):
    pool_url=[]
    for i in soup.find_all('tr',class_='odd'):
        pool=i.a['href']
        pool='https://yande.re'+pool.replace('show','zip')
        pool=[pool,i.find_all('a')[0].string.replace(' ','_')]
        pool_url.append(pool)
    for i in soup.find_all('tr',class_='even'):
        pool=i.a['href']
        pool='https://yande.re'+pool.replace('show','zip')
        pool=[pool,i.find_all('a')[0].string.replace(' ','_')]
        pool_url.append(pool)
    return pool_url

def login():
    try:
        session = requests.session()
        session.cookies = cj.LWPCookieJar(filename='ydcookies.txt')
        session.cookies.load(filename='ydcookies.txt', ignore_discard=True)
    except:
        session = requests.session()
        session.cookies = cj.LWPCookieJar()
        res = session.get('https://yande.re/user/login').content
        soup = BeautifulSoup(res, "lxml")
        csrf_token=soup.find_all('meta',attrs={'name': "csrf-token"})[0]['content']
 
        login_data = {
            'authenticity_token':csrf_token,
            'url': '/user/login',
            'user[name]':'your account',
            'user[password]':'your password',
            'commit':'Login',
        }
        session.post('https://yande.re/user/login', data=login_data)
        time.sleep(3)
        session.cookies.save(filename='ydcookies.txt', ignore_discard=True, ignore_expires=True)
    return session

def get_pool_ori(url,file_path,session):
    res = session.get(url[0]).content
    print("Downloading ZIP..."+url[1])
    with open(file_path+url[1]+'.zip', "wb") as f:
        f.write(res)
    print ("OK..."+url[1])
    return

def get_pool_jpeg(url,file_path,session):
    res = session.get(url[0]+'?jpeg=1').content
    print("Downloading ZIP(JPEG)..."+url[1])
    with open(file_path+url[1]+'.zip', "wb") as f:
        f.write(res)
    print ("OK..."+url[1])
    return
    
    
def get_pic_url(soup):
    pic_url=[]
    for i in soup.find_all('a',class_='thumb'):
        pic=i.find_all('span')
        pic=pic[0].string.strip('#pl ')
        pic_url.append(pic)
    return pic_url

def get_one_page(url,opener):
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
    
def main_pic():
    
    #login()
    #cookie = cj.LWPCookieJar()
    #cookie.load('ydcookies.txt')
    #handler = request.HTTPCookieProcessor(cookie)
    #opener = request.build_opener(handler)

    opener = request.build_opener()
    
    url = 'https://yande.re/post?tags=dakimakura'
    file_path='./imagemmm/'
    os.makedirs(file_path, exist_ok=True)
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    opener.addheaders = [ headers ]
    for n in range(1,2):
        url='https://yande.re/post?page='+str(n)+'&tags=himeno_sena'
        soup=get_one_page(url,opener)
        pic_url=get_pic_url(soup)
        for i in pic_url:
            soup=get_one_page(i,opener)
            pic_info=get_picinfo(soup)
            try:
                get_pic_ori(soup,file_path,pic_info)
            except:
                get_pic_larger(soup,file_path,pic_info)
    print ('Program Over.')
    
def main_pool():
    url='https://yande.re/pool?query=shiratama'
    file_path='./pool/'
    os.makedirs(file_path, exist_ok=True)
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    opener = request.build_opener()
    opener.addheaders = [ headers ]
    session=login()
    for n in range(1,2):
        url='https://yande.re/pool?query=shiratama'+'&page='+str(n)
        soup=get_one_page(url,opener)
        pool_url=get_pool_url(soup)
        for i in pool_url:
            get_pool_jpeg(i,file_path,session)
    print ('Program Over.')
    
main_pool()


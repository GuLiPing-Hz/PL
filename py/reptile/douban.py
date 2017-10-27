#!python3.4
#@ guliping

"""
网络爬虫

Beautifulsoup + request，urllib 编写的小巧爬虫 没有采用scrapy框架
"""

#pip install beautifulsoup4
from bs4 import BeautifulSoup
import http.cookiejar
import urllib.request
import http.client
import urllib.parse

import gzip
#import numpy
import pandas

class VisitUrl(object):
    """docstring for visit_url"""
    def __init__(self):
        super(VisitUrl, self).__init__()
        self.had_visited = []

    def visit(self,url):
        soup = None
        if(url == None or url == "" or (url in self.had_visited)):
            print("已经访问过了!!!",url)
            return soup

        self.had_visited.append(url)
        print("正在访问",url)

        #超慢的http访问,登录，记录cookie
        filename = 'cookie.txt'
        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cj = http.cookiejar.MozillaCookieJar(filename)
        handler = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(handler)

        opener.addheaders = [('Accept-Language','zh-CN'),('Connection','keep-alive'),("Accept-Encoding","gzip,utf-8")
            ,("Accept","text/plain"),("Content-type","application/x-www-form-urlencoded")
            ,('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]
        # postdata = urllib.parse.urlencode({'username':'jjhhh'
        #     ,'password':'e10adc3949ba59abbe56e057f20f883e','questionid':0,'answer':''}
        #     ).encode('utf-8')
        #登录的URL
        
        #模拟登录，并把cookie保存到变量
        # print(opener)
        try:
            result = opener.open(url)#,postdata)
            #cj.save(ignore_discard=True, ignore_expires=True)
            #保存cookie到cookie.txt中
            print(result.status, result.reason,type(result))

            data = ""#response.read()
            if result.info().get('Content-Encoding') == 'gzip':
                try:
                    data = gzip.decompress(result.read()).decode("utf-8")
                except UnicodeDecodeError as e:#对不能用utf-8 解密的网页，我们只能过滤掉了
                    pass
            else:
                try:
                    data = result.read().decode("utf-8")
                except UnicodeDecodeError as e:#对不能用utf-8 解密的网页，我们只能过滤掉了
                    pass

            soup = BeautifulSoup(data, 'html.parser')
        except urllib.error.HTTPError as e:#访问不了就再见
            print("http error :",url)
            pass
        except Exception as e:
            raise e
        
        return soup

    def visit_all(self,url):
        soup = self.visit(url)

        if(soup):
            tag_a_lst = soup.find_all("a")
            print("当前页的超链接：",tag_a_lst)
            for i in range(len(tag_a_lst)):
                item = tag_a_lst[i]
                print("*"*100)
                print(type(item),item)
                value = item.get('href')
                print("超链接地址:",url,value)

                if(value == "/"):#这还是访问当前地址，忽略
                    pass
                elif(value == "javascript:;"):#百度的按钮样式
                    pass
                elif(value.startswith("http")):
                    self.visit_all(value)
                elif(value.startswith("//")):
                    self.visit_all("http:"+value)
                else:
                    new_url = url
                    xiegang_split = url.split("/")
                    if(len(xiegang_split) > 3): # http://music.baidu.com 标准分出来应该是3个
                        pos_end = url.find("/",8) #取出主域名
                        if(pos_end != -1):
                            new_url = url[:pos_end]
                            print("新地址",new_url)
                    self.visit_all(new_url + value)

def get_douban():
    """
    爬取豆瓣网站的信息
    """

    visiter = VisitUrl()
    #visiter.visit_all("https://www.douban.com")
    visiter.visit_all("https://www.baidu.com")

if __name__ == '__main__':
    print("开始访问网站...")
    get_douban()
    print("访问到此结束")

    # url = "http://music.baidu.com/mall?from=pcweb_music_qrcode"
    # xiegang_split = url.split("/")
    # print(xiegang_split)
    # pos_end = url.rfind("/") #取出主域名
    # new_url = url
    # if(pos_end != -1):
    #     new_url = url[:pos_end]
    #     print("新地址",new_url)

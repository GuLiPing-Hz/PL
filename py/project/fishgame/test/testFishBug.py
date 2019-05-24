import codecs
# Http 模块
import http.client
import urllib.parse
# json解析模块
import json
HEADERS = {"Content-Type": "application/json", "Accept": "text/plain"}
def main_test_fish_bug():
    try:
        
        # https 本地地址
        # conn = http.client.HTTPSConnection("192.168.0.120:9191")
        # 本地地址
        # conn = http.client.HTTPConnection("192.168.0.120:9191")
        # 正式服地址
        conn = http.client.HTTPSConnection("122.226.180.199")
        tempHead = dict(HEADERS)
        # print(json_params)
        conn.request("GET", "/fanyu-portal/redPack?wx_unionid=oCG2N0gF7Pqd_uE92IrlGkDuIPt0&wares_id=tx2",None, tempHead)
        response = conn.getresponse()
        data = response.read()

    # print(type(data))
        print(response.status, response.reason,
              data.decode(), sep=' ; ')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass

def main_test_fish_bug2():
    # http 查询
    # "Accept": "text/html"
    # "Accept-Encoding":"utf-8"
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Accept-Encoding": "gzip", 'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    conn = http.client.HTTPSConnection("g.fanyu123.com")
    # cj.add_cookie_header()
    # https://g.fanyu123.com/fanyu-portal/redPack?wx_unionid=oCG2N0gF7Pqd_uE92IrlGkDuIPt0&wares_id=tx2
    try:
        conn.request("GET", "/fanyu-portal/redPack?wx_unionid=oCG2N0gF7Pqd_uE92IrlGkDuIPt0&wares_id=tx2", None, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass

if __name__ == '__main__':
    for i in range(100):
        print("test ",i)
        main_test_fish_bug()

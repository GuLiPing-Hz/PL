import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import urllib.request
import cv2
import numpy as np
# 随机数
import random

# For instance, consider this page source:

# <html>
#  <body>
#   <form id="loginForm">
#    <input name="username" type="text" />
#    <input name="password" type="password" />
#    <input name="continue" type="submit" value="Login" />
#    <input name="continue" type="button" value="Clear" />
#   </form>
# </body>
# <html>
# The form elements can be located like this:
# 	login_form = driver.find_element_by_xpath("/html/body/form[1]")
# 	login_form = driver.find_element_by_xpath("//form[1]")
# 	login_form = driver.find_element_by_xpath("//form[@id='loginForm']")

# 如果这个放到闭包中，出了闭包，页面的内容就会消失
Browser = webdriver.Chrome()


def get_tracks(width, type=1):
    v = 0
    tracks = []
    current = 0
    
    if type == 1:
        while current <= width:
            t = random.random()*0.3+0.05
            v0 = v
            v = v0 + 6 * t
            s = (v0 + v) / 2 * t
            current += s
            tracks.append(round(s))
    elif type == 2:
        mid = width*4/5
        while current <= width:
            t = random.random()*0.3+0.05
            if current < mid:  # 小余这个位置，以加速度a前进(simulate加速过程)
                a = 2
            else:  # 大于这个位置了，以加速度a前进(simulate减速过程)
                a = -3
            v0 = v
            v = v0 + a * t
            s = (v0 + v) / 2 * t
            current += s
            tracks.append(round(s))
    return tracks

def defend_with_tb(browser):
    pass
    # chrome_options = browser.ChromeOptions()
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--profile-directory=Default')
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-plugins-discovery");
    # chrome_options.add_argument("--start-maximized")
    # browser = browser.Chrome(chrome_options=chrome_options)
    # browser.delete_all_cookies()
    # browser.set_window_size(800,800)
    # browser.set_window_position(0,0)

def defend_with_tb2(browser):
    js1= "Object.defineProperties(navigator,{ webdriver:{ get: () => false } });"
    js2= "window.navigator.chrome = { runtime: {},  };"
    js3= "Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });"
    js4= "Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });"
    browser.execute_script(js1)
    browser.execute_script(js2)
    browser.execute_script(js3)
    browser.execute_script(js4)


def main_nike2(browser, url,targetUrl):
    defend_with_tb(browser)
    browser.get(url)
    defend_with_tb2(browser)
    # print(browser.current_url)
    # print(browser.page_source)
    # 跳转到指定的iframe
    browser.switch_to.frame(browser.find_element_by_id("J_loginIframe"))
    # time.sleep(1) #1秒钟等待。
    # print("*"*100 + "GLP\n\n\n")
    # print(browser.page_source)
    # browser.close()

    # try:
    # 	#10秒
    # 	element_mmdl = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "J_Quick2Static")))
    # 	print(element_mmdl)
    # finally:
    # 	browser.quit()

    # element_mmdl = browser.find_element_by_css_selector("#forget-pwd J_Quick2Static")
    # element_mmdl = browser.find_element_by_class_name("i.iconfont")
    # element_mmdl = browser.find_element_by_partial_link_text("密码登录")
    # element_mmdl = browser.find_element_by_id("J_Quick2Static")
    # element_mmdl = browser.find_element_by_xpath('//*[@id="J_Quick2Static"]')
    # //*表示匹配任意标签,我们这里只匹配i标签
    element_mmdl = browser.find_element_by_xpath('//i[@id="J_Quick2Static"]')
    element_mmdl.click()  # 点击密码登录
    # print(element_mmdl)

    element_zh = browser.find_element_by_xpath(
        '//input[@id="TPL_username_1"]')  # 账号
    # element_zh.click() #输入框点击会报错
    element_zh.send_keys('260140429@qq.com')
    time.sleep(0.5)

    fail_try = 0
    while not browser.current_url.startswith(targetUrl):
        try:
            element_mm = browser.find_element_by_xpath(
                '//input[@id="TPL_password_1"]')  # 密码
            # element_mm.click()
            element_mm.send_keys('xr123456')
            time.sleep(1)

            try:
                element_hk = browser.find_element_by_xpath(
                    '//span[@id="nc_1_n1z"]')  # 滑块
                # 下面进行一个序列化操作。。
                actions = ActionChains(browser)
                actions.click_and_hold(on_element=element_hk)  # 首先鼠标按下并保持

                tracks = get_tracks(320)
                for track in tracks:
                    actions.move_by_offset(
                        xoffset=track, yoffset=0).perform()  # 鼠标位移
            except Exception as e:
                pass

            # actions.move_by_offset(xoffset=300, yoffset=0)
            # actions.release(on_element=element_hk).perform()# 鼠标抬起

            time.sleep(3)
            element_btn_dl = browser.find_element_by_xpath(
                '//button[@id="J_SubmitStatic"]')  # 登录按钮
            element_btn_dl.click()

            time.sleep(1)
            element_msg = browser.find_element_by_xpath(
                '//div[@id="J_Message"]')  # 登录按钮
            if not element_msg.is_displayed():
                print("登录成功")
                break
            else:
                fail_try = fail_try + 1
                print("登录失败",fail_try)
        except Exception as e:
            time.sleep(3)
            print(e)

    print(browser.page_source)
    # browser.quit()


if __name__ == '__main__':
    url = r"https://login.tmall.com/?spm=a220o.1000855.a2226mz.2.1f627ecbpROZxN&redirectURL=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da1z10.4-b-s.w5003-21076098180.3.31c9174a5Yi3QI%26id%3D576640717890%26scene%3Dtaobao_shop%26sku_properties%3D1627207%3A2471828828"
    main_nike2(Browser, url,"https://detail.tmall.com/item.htm")

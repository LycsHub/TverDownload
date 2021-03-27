'''
Author: harry
Date: 2021-03-26 10:17:24
LastEditTime: 2021-03-26 20:00:12
LastEditors: harry
Description: edited by harry
FilePath: /tver/youtudltver.py
E-mail: lycshub@gmail.com
'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-


from __future__ import unicode_literals
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import re
import requests
import youtube_dl



# 定义youtubedl输出日志格式
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

# 控制下载状态
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    if d['status'] == 'downloading':
        p = d['_percent_str']
        p = p.replace('%','')
        print('\r'+d['filename'], d['_percent_str'], d['_eta_str'],end='')




# 若使用chrome
# capabilities = webdriver.DesiredCapabilities.CHROME
# capabilities['pageLoadStrategy'] = "none"
# driver = webdriver.Chrome(executable_path='./')

def getDLlink(tver_url):
    # 异步的方式进行浏览器的开启
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    capabilities['pageLoadStrategy'] = "none"
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.delete_all_cookies()
    
    driver.get(tver_url)

    try:
        sleep(10)
        driver.execute_script("window.parent.enquete.closeEnquete();") 
        sleep(10)
        # 以video标签作为基准
        data_account = driver.find_element_by_css_selector('video').get_attribute('data-account')
        # 以父元素为基准定位第一个子元素
        data_video_id = driver.find_element_by_id('playerWrapper').find_element_by_tag_name('div').get_attribute('data-video-id')
        # print(data_account)
        # print(data_video_id)
    except Exception:
        pass

    driver.delete_all_cookies()
    driver.quit()
    # 拼接下载url
    tver_download_link = "http://players.brightcove.net/"+data_account+"/default_default/index.html?videoId="+data_video_id
    return tver_download_link


if __name__ == '__main__':
    # 用户输入
    tver_url = input("pls input a tver vedio link:\n")
    # 调用youtebl download video
    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'proxy': 'socks5://127.0.0.1:1080',# 代理服务器,如果在日本网络环境下可以注释
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([getDLlink(tver_url)])
        # ydl.download(['https://www.bilibili.com/video/BV1TK4y1D7oa?spm_id_from=333.851.b_7265636f6d6d656e64.1'])



import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import time
# import os

def scrapingjobinfo():
    db_url = 'mongodb://192.168.219.105:27017'
    url = 'https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A'
    #     
    driver = webdriver.Chrome(executable_path='/home/hanyohan/Documents/Develop/chromedriver')
    driver.get(url)
    
    s_ul = driver.find_element_by_class_name('ann_list')
    s_li = s_ul.find_elements_by_tag_name('li')
    # 
    print()
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        for fs_li in s_li:            
            fs_li.find_element_by_tag_name('button').click()            
            driver.switch_to_window(driver.window_handles[-1])
            html = driver.page_source
            soup = BeautifulSoup(html,'lxml')
            div = soup.select('div[class*="type_text"]')
            # 
            post_title = soup.select_one('h4').string
            term = div[0].string
            accept = div[1].stirng
            target = div[2].stirng
            schedule = div[3].stirng
            spot = div[4].stirng
            content = div[5].stirng
            # 
            data = {
                    'title':post_title,
                    'term':term,
                    'accept':accept,
                    'target':target,
                    'schedule':schedule,
                    'spot':spot,
                    'content':content,
                    'create_date':datetime.datetime.now()
            }
            # 
            infor = mydb.startupinfo.insert_one(data)     
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(10)

scrapingjobinfo()        
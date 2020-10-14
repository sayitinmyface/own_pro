
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import datetime
import time

    
# import os

def scrapingjobinfo():
    db_url = 'mongodb://192.168.219.116:27017'
    url = 'https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A'
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(url)
    # 
    s_li = driver.find_elements(By.CSS_SELECTOR,'[id*="liArea"]')
    time = str(datetime.datetime.now())
    # Options.add_argument(driver.maximize_window)
    
    # 
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        try:
            while not driver.find_element_by_class_name('btn_listAll') is None:
                driver.find_element_by_class_name('btn_listAll').click()               
        except:
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        # 
        # time.sleep(3)
        for fs_li in s_li:            
            # if fs_li.find_element_by_class_name('ann_list_group05').text != '시설·공간·보육':
            screen_n = str(datetime.datetime.now())
            fs_li.find_element_by_class_name('bt_Nwindow').click()                        
            driver.switch_to_window(driver.window_handles[-1])
            # 
            html = driver.page_source
            soup = BeautifulSoup(html,'lxml')
            div = soup.select('div[class*="type_text"]')
            tbody = soup.select_one('tbody')
            td = tbody.select('td')
            # 
            str_content = ''
            for f_div in div:
                str_content += str(f_div.string)
            # 
            str_content = str_content.replace('None','')
            str_content = str_content.replace('\t','')    
            # 
            post_title = soup.select_one('h4').string
            organization = td[0].string.strip()
            organization_sub = td[1].string.strip()
            department = td[2].string.strip()
            contact_address = td[3].string.strip()
            term = td[4].string.strip()
            support = td[5].string.strip()
            local = td[6].string.strip()
            period = td[7].string.strip()
            subject = td[8].string.strip()
            age = td[9].string.strip()
            content = str_content
            # 
            collection = mydb['startupinfo']                

            data = {
                    'post_title':post_title,
                    'organization':organization,
                    'organization_sub':organization_sub,
                    'department':department,
                    'contact_address':contact_address,
                    'term':term,
                    'support':support,
                    'local':local,
                    'period':period,
                    'subject':subject,
                    'age':age,
                    'content':content,
                    'create_date':datetime.datetime.now()
            }
            # 
            infor = mydb.startupinfo.insert_one(data)     
            driver.save_screenshot(f'./static/images/{screen_n}.png')
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
# 
scrapingjobinfo()        
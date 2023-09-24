from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time
import os
from bs4 import BeautifulSoup
import requests
from requests import exceptions
import re

def download_file(filename, url):
    while True:
        try:
            with open(f"{filename}", 'wb') as f:
                resp = requests.get(url, headers={'referer':'https://bestdori.com', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}, ).content
                f.write(resp)
                break

        except ( exceptions.ChunkedEncodingError, 
                 exceptions.Timeout,
                 exceptions.ConnectionError ):
            continue



service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://bestdori.com')
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[2]/div[3]/a').click()


char = '香澄'

def get_info(story_url):
    driver.get(story_url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div/div/div/a[2]').click()
    time.sleep(5)
    a = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[3]/div[4]/div[4]')
    html = str(a.get_attribute('innerHTML'))
    soup = BeautifulSoup(html, 'html.parser')

    for i in soup.find_all('a', {'class':'box bg-white download-container'}):
        try:
            spk = i.find_all('span')[1].text.strip()
            trsc = re.sub('[\s+]', '', i.find_all('div', {'class':'column'})[1].text).strip()
            url = 'https://bestdori.com'+i.find('a', {'download':''})['href'].strip()
            save_dir = f'./dataset/{char}/'
            fname = os.path.basename(url)
            save_loc = os.path.join(save_dir, fname)

            if spk != char:
                continue
            print(spk)
            print(trsc)
            print(url)
            print('\n')
            download_file(save_loc, url)
            open(f'{char}.txt', 'a+', encoding='utf-8').write(f'{save_loc}|{trsc}\n')
        except:
            continue


'''
101 - 127
1 - 20
128 - 142
393 - 407
'''

[range(1, 21),
range(101, 127),
range(128, 143),
range(393, 408)]
b = list(range(128, 143)) + list(range(393, 408))
for i in b:
    get_info(f'https://bestdori.com/tool/storyviewer/band/jp/{i}')

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

df = pd.DataFrame(columns=['title', 'link', 'thumbnail','likes','comments'])
comment_dataframe = pd.DataFrame(columns=['author','comment'])


driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
wd = webdriver.Chrome(driver_path)

url = ["https://www.youtube.com/watch?v=Pp6CO2_YEDE", "https://www.youtube.com/watch?v=TXHB9wL4WFg","https://www.youtube.com/watch?v=EgFobac32IE", "https://www.youtube.com/watch?v=O2XY3Y7JIa0"]


wd.get(url[0])
time.sleep(5)
wait = WebDriverWait(wd, 20)
for i in range(5):
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
    time.sleep(5)
soup = bs(wd.page_source,'lxml')

#source = requests.get(url[0]).text

#soup = bs(source,'lxml')

meta_data = soup.findAll("meta")
title = soup.find("meta",itemprop='name')['content']
link = soup.find("meta",property="og:video:url")['content']
thumbnail = soup.find("meta",property="og:image")['content']
likes = soup.find('yt-formatted-string', {'class': 'style-scope ytd-toggle-button-renderer style-text'}).text
comments = soup.find('h2',id='count').text.replace('Comments','').strip()

comments_all = [i.text.strip() for i in soup.findAll(id='content-text')]
comment_author = [i.text.strip() for i in soup.findAll('a',id='author-text')]

comment_dataframe['author'] = comment_author
comment_dataframe['comment'] = comments_all


print(f"{title},\n{link}\n{thumbnail},\n{likes},\n{comments}")
print(comment_dataframe.to_string())

wd.quit()
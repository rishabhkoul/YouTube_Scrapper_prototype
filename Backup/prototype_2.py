import base64
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

driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
text = []
channel = "https://www.youtube.com/c/TheRanveerShowClips/videos"
df = pd.DataFrame(columns=['title', 'link', 'thumbnail','likes','comments'])
comment_data = pd.DataFrame(columns=['channel_name', 'author', 'comments'])

def get_50_url(channel_url,no_of_urls):
    try:
        with webdriver.Chrome(driver_path) as wd:
            wait = WebDriverWait(wd, 20)
            wd.get(channel_url)
            time.sleep(10)

            for i in range(4):
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(4)
            while len(text) < 51:
                for link in wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='thumbnail']"))):
                    text.append(link.get_attribute('href'))

            url_50 = text[1:no_of_urls+1]

            print(url_50)
            print(len(url_50))
            return url_50

    except TimeoutError as e:
        print(e)


def get_title_link_thumbnail_comments(url):
    try:

        wd = webdriver.Chrome(driver_path)
        wd.get(url)
        time.sleep(5)
        wait = WebDriverWait(wd, 20)
        for i in range(5):
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
            time.sleep(5)

        soup = bs(wd.page_source, 'lxml')
        title = soup.find("meta", itemprop='name')['content']
        link = soup.find("meta", property="og:video:url")['content']
        thumbnail = soup.find("meta", property="og:image")['content']
        channel_name = soup.find('a', {'class': "yt-simple-endpoint style-scope yt-formatted-string"}).text
        thumbnail_bs4 = base64.b64encode(requests.get(thumbnail).content)
        likes = soup.find('yt-formatted-string', {'class': 'style-scope ytd-toggle-button-renderer style-text'}).text
        comments = soup.find('h2', id='count').text.replace('Comments', '').strip()
        data = {'title': title, 'link': link, 'thumbnail': thumbnail,'likes':likes,'comments':comments}

        # to save comments in a data frame
        comment_df = pd.DataFrame(columns=['channel_name', 'author', 'comments'])
        comments_all = [i.text.strip() for i in soup.findAll(id='content-text')]
        comment_author = [i.text.strip() for i in soup.findAll('a', id='author-text')]
        comment_df['author'] = comment_author
        comment_df['comments'] = comments_all
        comment_df['channel_name'] = channel_name



        return [data,comment_df]
    except Exception as e:
        print(e)


for n,i in enumerate(get_50_url(channel,no_of_urls=4)):
    list_of_data = get_title_link_thumbnail_comments(i)
    df = pd.concat([df, pd.DataFrame(list_of_data[0],index=[n])], axis=0)
    comment_data = pd.concat([comment_data,list_of_data[1]],axis=0)

df.to_csv("channel_data.csv")
comment_data.to_csv("comment_data.csv")
print(df.to_string())
print(comment_data.to_string())

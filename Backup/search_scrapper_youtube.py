import logging
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
logging.basicConfig(filename='search_scrapper.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
search = str(input("Enter URL")).strip().replace(" ","+")
search_url = f'https://www.youtube.com/results?search_query={search}'

df = pd.DataFrame(columns=['title','views','category','link'])


def get_urls(url):
    list_url = []
    try:
        with Chrome(driver_path) as wd:
            wait = WebDriverWait(wd,20)
            wd.get(url)
            time.sleep(5)

            for i in range(18):
                wait.until(ec.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(3)

            for i in wd.find_elements(By.XPATH,'//a[@id="video-title"]'):
                list_url.append(i.get_attribute('href'))

            list_url = list_url[1:51]
            logging.info(list_url)
            logging.info(len(list_url))
            return list_url


    except Exception as e:
        logging.error(e)
    finally:
        wd.quit()

def get_video_data(video_url):
    try:
        source = requests.get(video_url).text
        soup = bs(source,'lxml')
        title = soup.find("meta", itemprop='name')['content']
        views = soup.find("meta", itemprop='interactionCount')['content']
        category = soup.find("meta", itemprop='genre')['content']
        link = soup.find("meta", property="og:video:url")['content']
        return {'title':title,'views':views,'category':category,'link':link}

    except Exception as e:
        logging.error(e)

for n,i in enumerate(get_urls(search_url)):
    df = pd.concat([df, pd.DataFrame(get_video_data(i),index=[n])], axis=0)
    df.to_csv('search_urls.csv')
logging.info(df.to_string())
print(df.to_string())
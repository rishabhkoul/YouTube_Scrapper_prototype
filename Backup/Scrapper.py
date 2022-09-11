import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

logging.basicConfig(filename='scrapper.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

list_url = ["https://www.youtube.com/watch?v=Pp6CO2_YEDE", "https://www.youtube.com/watch?v=TXHB9wL4WFg",
            "https://www.youtube.com/watch?v=EgFobac32IE", "https://www.youtube.com/watch?v=O2XY3Y7JIa0"]
driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
text = []


def scrap_data(url):
    try:
        dict = {}
        with webdriver.Chrome(driver_path) as wd:
            wait = WebDriverWait(wd, 20)
            wd.get(url)
            time.sleep(10)

            for i in range(3):
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(4)

            title = wd.find_element(By.XPATH, "/html/head/meta[8]").get_attribute('content')

            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='top-level-buttons-computed']")))
            likes = wd.find_element(By.XPATH,
                                    "//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").text

            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sections']")))
            comment = wd.find_element(By.XPATH, "//*[@id='count']/yt-formatted-string").text.replace('Comments',
                                                                                                     '').strip()

            # wait.until(EC.presence_of_element_located((By.XPATH,"/html/head/meta[7]")))
            video_link = wd.find_element(By.XPATH, "/html/head/meta[7]").get_attribute('content')

            # wait.until(EC.presence_of_element_located((By.XPATH,"/html/head/meta[9]")))
            video_thumbnail_link = wd.find_element(By.XPATH, "/html/head/meta[9]").get_attribute('content')

        dict['title'] = title
        dict['likes'] = likes
        dict['comments'] = comment
        dict['video_link'] = video_link
        dict['thumbnail_link'] = video_thumbnail_link
        return dict

    except Exception as e:
        logging.error(e)
    finally:
        wd.quit()


df = pd.DataFrame(columns=['title', 'likes', 'comments', 'video_link', 'thumbnail_link'])
for i in list_url:
    logging.info(scrap_data(i))
    df = pd.concat([df, pd.DataFrame([scrap_data(i)])], axis=0)

logging.info(df)

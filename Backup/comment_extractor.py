import logging
logging.basicConfig(filename='comment_scrapper.log',level=logging.DEBUG,format="%(asctime)s %(levelname)s %(message)s")
import time


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

data = []
url = "https://www.youtube.com/watch?v=Pp6CO2_YEDE"
driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"

with webdriver.Chrome(driver_path) as wd:
    try:
        wait = WebDriverWait(wd,15)
        wd.get(url)


        for i in range(10):
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)   #By.TAG_NAME is to search by locator such as class, css, id and Keys is special key codes, END key takes us to bottom of page
            time.sleep(2)

        for com in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
            data.append(com.text)
        logging.info(data)
        logging.info("No of comments is %d",len(data))
    except Exception as e:
        logging.error(e)


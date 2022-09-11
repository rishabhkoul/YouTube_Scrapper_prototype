import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

list_url = ["https://www.youtube.com/c/TheRanveerShowClips/videos","https://www.youtube.com/watch?v=TXHB9wL4WFg","https://www.youtube.com/watch?v=EgFobac32IE","https://www.youtube.com/watch?v=O2XY3Y7JIa0"]
driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
text = []

"""
try:
    with webdriver.Chrome(driver_path) as wd:
        wait = WebDriverWait(wd,20)
        wd.get(list_url[2])
        time.sleep(10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='title']/h1")))
        title = wd.find_element(By.XPATH, "//div[@id='title']/h1").text
        for i in range(3):
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
            time.sleep(4)



        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='top-level-buttons-computed']")))
        likes = wd.find_element(By.XPATH, "//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").text

        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='sections']")))
        comment = wd.find_element(By.XPATH, "//*[@id='count']/yt-formatted-string").text.replace('Comments','').strip()

        #wait.until(EC.presence_of_element_located((By.XPATH,"/html/head/meta[7]")))
        video_link = wd.find_element(By.XPATH, "/html/head/meta[7]").get_attribute('content')

        #wait.until(EC.presence_of_element_located((By.XPATH,"/html/head/meta[9]")))
        video_thumbnail_link = wd.find_element(By.XPATH, "/html/head/meta[9]").get_attribute('content')

        print(title,likes,comment,video_link,video_thumbnail_link)

except TimeoutError as e:
    print(e)
    wd.quit()
"""
try:
    with webdriver.Chrome(driver_path) as wd:
        wait = WebDriverWait(wd, 20)
        wd.get(list_url[0])
        time.sleep(10)

        for i in range(4):
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
            time.sleep(4)
        while len(text) < 51:
            for link in wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='thumbnail']"))):
                text.append(link.get_attribute('href'))

        url_50 = text[1:51]

        print(url_50)
        print(len(url_50))

except TimeoutError as e:
    print(e)
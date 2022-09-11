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
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin


driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"
text = []
channel = "https://www.youtube.com/c/TheRanveerShowClips/videos"
df = pd.DataFrame(columns=['title', 'link', 'thumbnail'])

def get_50_url(channel_url):
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

            url_50 = text[1:51]

            print(url_50)
            print(len(url_50))
            wd.quit()
            return url_50

    except TimeoutError as e:
        print(e)


def get_title_link_thumbnail(url):
    try:
        source = requests.get(url).text
        soup = bs(source, 'lxml')
        title = soup.find("meta", itemprop='name')['content']
        link = soup.find("meta", property="og:url")['content']
        thumbnail = soup.find("meta", property="og:image")['content']
        thumbnail_bs4 = base64.b64encode(requests.get(thumbnail).content)
        data = {'title': title, 'link': link, 'thumbnail': thumbnail}
        return data
    except Exception as e:
        print(e)




app = Flask(__name__)

@app.route("/",methods=['GET'])
@cross_origin()

def homePage():
    return render_template("index.html")

@app.route('/scrapper',methods=['POST','GET'])
@cross_origin()

def index():
    if request.method == 'POST':
        try:
            data = []
            url = request.form['content']
            for i in get_50_url(url):
                data.append(get_title_link_thumbnail(i))
            return render_template('results.html',data = data)
        except Exception as e:
            pass


if __name__ == '__main__':
    app.run(debug=True)

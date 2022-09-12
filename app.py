import base64
import json
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
import pymongo
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


client = pymongo.MongoClient("mongodb+srv://Rishabh:Mongodb2@cluster0.lhaw5.mongodb.net/?retryWrites=true&w=majority")
db = client.test




df = pd.DataFrame(columns=['title', 'link', 'thumbnail'])
comment_data = pd.DataFrame(columns=['channel_name', 'author', 'comments'])

def get_50_url(channel_url,no_of_urls):
    try:
        with webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) as wd:
            text = []
            wait = WebDriverWait(wd, 15)
            wd.get(channel_url)
            time.sleep(10)

            for i in range(4):
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(4)


            for link in wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='thumbnail']"))):
                    text.append(link.get_attribute('href'))

            url_50 = text[1:no_of_urls+1]
            return url_50
    except TimeoutError as t:
        print(t)
    except Exception as e:
        print(e)
    

def get_title_link_thumbnail_comments(url):
    try:
        with webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) as wd:
            wait = WebDriverWait(wd, 20)
            
            wd.get(url)
            
            time.sleep(5)
            
            for i in range(5):
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(5)

            soup = bs(wd.page_source, 'lxml')
            title = soup.find("meta", itemprop='name')['content']
            link = soup.find("meta", property="og:url")['content']
            thumbnail = soup.find("meta", property="og:image")['content']

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "yt-formatted-string")))

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

def to_pymongo(dataframe):
    try:
        database = client['youtube_scrapper']
        collection = database['comments']
        result_json = dataframe.to_json(orient='index')
        parsed = json.loads(result_json)
        collection.insert_many([parsed])
  
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
            print(url)
            url_list = get_50_url(url,no_of_urls=4)
            print(url_list)
            time.sleep(5)
            for i in url_list:
                list_of_data = get_title_link_thumbnail_comments(i)
                data.append(list_of_data[0])
                to_pymongo(dataframe=list_of_data[1])
            
            return render_template('results.html',data = data)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app.run(debug=False)










"""
for n,i in enumerate(get_50_url(channel,no_of_urls=4)):
    list_of_data = get_title_link_thumbnail_comments(i)
    to_database(list_of_data[0])
    df = pd.concat([df, pd.DataFrame(list_of_data[0],index=[n])], axis=0)
    comment_data = pd.concat([comment_data,list_of_data[1]],axis=0)


print(df.to_string())
print(comment_data.to_string())
"""

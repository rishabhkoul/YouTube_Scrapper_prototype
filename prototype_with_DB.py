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
import mysql.connector as connector
import pymongo
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import logging

logging.basicConfig(filename='scrapper.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

mydb = connector.connect(host="localhost", user='root', password="Zenfone@2")
cursor = mydb.cursor()

client = pymongo.MongoClient("mongodb+srv://Rishabh:Mongodb2@cluster0.lhaw5.mongodb.net/?retryWrites=true&w=majority")
db = client.test


driver_path = r"C:\Users\Lenovo\iNeuron\ImageScrapper\chromedriver.exe"

channel = "https://www.youtube.com/c/TheRanveerShowClips/videos"
df = pd.DataFrame(columns=['title', 'link', 'thumbnail'])
comment_data = pd.DataFrame(columns=['channel_name', 'author', 'comments'])

def get_50_url(channel_url,no_of_urls):
    try:
        text = []
        with webdriver.Chrome("chromedriver.exe") as wd:
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

            logging.info(f"Scrapper urls are {url_50}")
            logging.info(f"No. of urls scrapped {len(url_50)}")
            #wd.quit()
            return url_50

    except TimeoutError as e:
        logging.info("Error occurred while getting URLs")
        logging.error(e)


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
        link = soup.find("meta", property="og:url")['content']
        thumbnail = soup.find("meta", property="og:image")['content']

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "yt-formatted-string")))

        channel_name = soup.find('a', {'class': "yt-simple-endpoint style-scope yt-formatted-string"}).text
        thumbnail_bs4 = base64.b64encode(requests.get(thumbnail).content)
        likes = soup.find('yt-formatted-string', {'class': 'style-scope ytd-toggle-button-renderer style-text'}).text
        comments = soup.find('h2', id='count').text.replace('Comments', '').strip()
        data = {'title': title, 'link': link, 'thumbnail': thumbnail,'likes':likes,'comments':comments}
        logging.info(data)

        # to save comments in a data frame
        comment_df = pd.DataFrame(columns=['channel_name', 'author', 'comments'])
        comments_all = [i.text.strip() for i in soup.findAll(id='content-text')]
        comment_author = [i.text.strip() for i in soup.findAll('a', id='author-text')]
        comment_df['author'] = comment_author
        comment_df['comments'] = comments_all
        comment_df['channel_name'] = channel_name
        wd.quit()


        return [data,comment_df]
    except Exception as e:
        logging.info('Error occurred while getting video data')
        logging.error(e)

def to_database(data):
    # data must be a dictionary
    try:
        cursor.execute('create database if not exists scrapper_test')
        cursor.execute("create table if not exists scrapper_test.video_data(title varchar(255),link varchar(255),thumbnail varchar(255),likes varchar(20),comments varchar(20))")

        columns = ', '.join("`" + str(x) + "`" for x in data.keys())
        values = ', '.join('"' + str(x) + '"' for x in data.values())

        # to mysql database
        cursor.execute("insert into scrapper_test.video_data values(%s)" % values)
        mydb.commit()
    except Exception as e:
        logging.info("Error occurred while adding data to database")
        logging.error(e)

def to_pymongo(dataframe):
    try:
        database = client['youtube_scrapper']
        collection = database['comments']
        result_json = dataframe.to_json(orient='index')
        parsed = json.loads(result_json)
        collection.insert_many([parsed])
        logging.info(parsed)
    except Exception as e:
        logging.error(e)



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
            for n,i in enumerate(get_50_url(url,no_of_urls=4)):
                list_of_data = get_title_link_thumbnail_comments(i)
                data.append(list_of_data[0])
                to_database(list_of_data[0])
                to_pymongo(dataframe=list_of_data[1])
            logging.info(data[0])
            return render_template('results.html',data = data)
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    app.run(debug=True)










"""
for n,i in enumerate(get_50_url(channel,no_of_urls=4)):
    list_of_data = get_title_link_thumbnail_comments(i)
    to_database(list_of_data[0])
    df = pd.concat([df, pd.DataFrame(list_of_data[0],index=[n])], axis=0)
    comment_data = pd.concat([comment_data,list_of_data[1]],axis=0)


print(df.to_string())
print(comment_data.to_string())
"""
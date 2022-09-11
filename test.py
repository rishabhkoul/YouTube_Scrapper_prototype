import json

import pymongo
import pandas as pd



client = pymongo.MongoClient("mongodb+srv://Rishabh:Mongodb2@cluster0.lhaw5.mongodb.net/?retryWrites=true&w=majority")
db = client.test
df = pd.read_csv(r"C:\Users\Lenovo\PycharmProjects\pythonProject1\Backup\comment_data.csv")
df.drop("Unnamed: 0",inplace=True,axis=1)

database = client['youtube_scrapper']
collection = df['comments']
result_json = df.to_json(orient='index')
parsed = json.loads(result_json)
print([parsed])
#collection.insert_many(parsed)

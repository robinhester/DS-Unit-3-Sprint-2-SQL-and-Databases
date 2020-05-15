import pandas as pd
import sqlite3, os
from dotenv import load_dotenv
import pymongo


DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "..",
                            "module1-introduction-to-sql",
                            "rpg_db.sqlite3")

sq_conn = sqlite3.connect(DATA_FILEPATH)

rpgdb = pd.read_sql_query("Select * From charactercreator_character", sq_conn)

print(rpgdb.head())
print("----------------------")
print(type(rpgdb))

rpg_dict = rpgdb.to_dict('index')
print('----------------------')
# print(rpg_dict)
print(type(rpg_dict))

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri)

db = client.rpg_database

collection = db.charactercreator

collection.insert_many(rpg_dict)

character = list(collection.find({"name": "Minus c"}))
print('-----------------------')
print(character)

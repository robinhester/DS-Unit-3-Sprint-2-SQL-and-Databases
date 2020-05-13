# column names Survived,Pclass,Name,Sex,Age,
# Siblings/Spouses Aboard, Parents/Children Aboard,Fare
# inspect what kind of datatypes would be needed
# integer columns - survived(0/1 boolean)
# Pclass, Age, Siblings, Parents, Fare

import pandas as pd 
import os, sqlite3, psycopg2
import numpy as np
from dotenv import load_dotenv
from psycopg2.extras import execute_values


DATA_FILEPATH = os.path.join(os.path.dirname(__file__),"..",
                            "module1-introduction-to-sql",
                            "rpg_db.sqlite3")

print("------------------------------")

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
# connect to pg db
load_dotenv()

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PW = os.getenv("DB_PW", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PW, host=DB_HOST)
print("------------------------------------------------")
print(type(connection)) #> <class 'psycopg2.extensions.connection'>

cursor = connection.cursor()
print("------------------------------------------------")
print(type(cursor)) #> <class 'psycopg2.extensions.cursor'>


cursor.execute(DATA_FILEPATH)


execute_values(cursor, insert_data, list_to_tuples)

connection.commit()

cursor.close()
connection.close()
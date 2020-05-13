# column names Survived,Pclass,Name,Sex,Age,
# Siblings/Spouses Aboard, Parents/Children Aboard,Fare
# inspect what kind of datatypes would be needed
# integer columns - survived(0/1 boolean)
# Pclass, Age, Siblings, Parents, Fare

import pandas as pd 
import os, psycopg2
import numpy as np
from dotenv import load_dotenv
from psycopg2.extras import execute_values


CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "titanic.csv")

titanic = pd.read_csv(CSV_FILEPATH)
print(titanic.head())

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

# create table
create_table =  """
                DROP TABLE IF EXISTS titanic;
                CREATE TABLE IF NOT EXISTS titanic (
                    id SERIAL PRIMARY KEY,
                    "Survived" int4,
                    "Pclass" int4,
                    "Name" text,
                    "Sex" text,
                    "Age" int4,
                    "Siblings/Spouses Aboard" int4,
                    "Parents/Children Aboard" int4,
                    "Fare" float8
);
                """

cursor.execute(create_table)


# insert titanic data 

insert_data = """
            INSERT INTO titanic(
                                Survived, Pclass, Name, 
                                Sex, Age, Siblings/Spouse Aboard,
                                Parents/Children Aboard, Fare   
                                )
                """

list_to_tuples = list(titanic.to_records(index=False))

execute_values(cursor, insert_data, list_to_tuples)

connection.commit()

cursor.close()
connection.close()

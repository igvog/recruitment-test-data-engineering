#!/usr/bin/env python
import csv
import json
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy

DB_NAME = 'codetest'

config = {
  'user': 'codetest',
  'password': 'swordfish',
  'database': DB_NAME,
  'host': "database",
}

# Connecting to Database
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Successfully connected to:", DB_NAME )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something wrong with password/username")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit()

try:
    with open('/data/people.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        id_count = cursor.lastrowid
        for row in reader:
            cursor.execute(
    """
    insert ignore into peoples
    (peoples_id, given_name, family_name, date_of_birth, place_of_birth)
    values (%(peoples_id)s, %(given_name)s, %(family_name)s, %(date_of_birth)s, %(place_of_birth)s)
    """, (id_count, row[0],row[1], row[2], row[3]))
            id_count = cursor.lastrowid + 1
        print("Successfully imported peoples csv")
except IOError:
    print("Can't read peoples csv file")



# connect to the database
#engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
#connection = engine.connect()

#metadata = sqlalchemy.schema.MetaData(engine)

# make an ORM object to refer to the table
#peoples = sqlalchemy.schema.Table('peoples', metadata, autoload=True, autoload_with=engine)
#with open('/data/people.csv') as csv_file:
#  reader = csv.reader(csv_file)
#  next(reader)
#  for row in reader: 
#    connection.execute(peoples.insert().values(
#      given_name = row[0],
#      family_name = row[1],
#      date_of_birth = row[2],
#      place_of_birth = row[3],
#      ))

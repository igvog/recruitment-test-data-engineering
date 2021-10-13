#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import mysql.connector
from mysql.connector import errorcode
import config as cfg

mydb = mysql.connector.connect(
    host = cfg.database_name, 
    user = cfg.database_user, 
    password = cfg.database_password, 
    charset = cfg.database_charset)
    
cursor = mydb.cursor()
cursor.execute("use codetest")
print("db connected")

for command in cfg.uft_commands:
    cursor.execute(command)

print("utf commands run")

cursor.execute("drop table if exists peoples, country, county, city;")
print("tables drop")

for table_name, command in cfg.tables.items():
    cursor.execute(command)
    print("table created " + table_name)
    
try:
    with open('/data/people.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        id_count = cursor.lastrowid
        for row in reader:
            cursor.execute(
                (cfg.insert_tables["peoples"]), (id_count, row[0], row[1], row[2], row[3]))
            id_count = cursor.lastrowid + 1
except IOError:
    print("Error with peoples csv file")

try:
    with open('/data/places.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        country_dict = {}
        county_dict = {}

        for row in reader:

            if row[2] in country_dict:
                country_id = country_dict[row[2]]
            else:
                country_dict[row[2]] = cursor.lastrowid
                country_id = country_dict[row[2]]

            if row[1] in county_dict:
                county_id = county_dict[row[1]]
            else:
                county_dict[row[1]] = cursor.lastrowid
                county_id = county_dict[row[1]]

            data_country = (country_id, row[2])
            data_county = (county_id, row[1], country_id)
            data_city = (cursor.lastrowid + 1, row[0], county_id)
            cursor.execute(
                cfg.insert_tables["country"]
                , data_country)
            cursor.execute(
                cfg.insert_tables["county"]
                , data_county)
            cursor.execute(
                cfg.insert_tables["city"]
                , data_city)
except IOError:
    print("Error with places csv file")

cursor.execute(cfg.peoples_table_update)
print("peoples table foreign key update")

cursor.execute(cfg.main_query)
print("main query run")

main_data = cursor.fetchall()

try:
    with open('/data/task.json', 'w') as json_file:
        rows = {}
        for i in main_data:
            query_row = {i[0] : i[1]}
            rows.update(query_row)
        json.dump(rows, json_file, separators=(',', ':'))
except IOError:
    print("Error with output file")

print("Data loaded")

## Close connection
mydb.commit()
cursor.close()
mydb.close()
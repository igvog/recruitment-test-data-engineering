#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(host="database", user="codetest", password="swordfish", charset='utf8')
cursor = mydb.cursor()
cursor.execute("use codetest")
print("db connected")

cursor.execute('SET NAMES utf8;') 
cursor.execute('SET CHARACTER SET utf8;') 
cursor.execute('SET character_set_connection=utf8;')


cursor.execute("drop table if exists peoples, country, county, city;")
cursor.execute(
    """
    create table country (
	country_id integer auto_increment not null,
	country_name varchar(255),
	primary key(country_id)
    )
    """
            )
cursor.execute(
    """
    create table county (
	county_id integer auto_increment not null,
	county_name varchar(255), 
	country_id int ,
    primary key(county_id),
    constraint forkey_country foreign key(country_id) references country(country_id)
    )
    """
            )
cursor.execute(
    """
    create table city (
	city_id integer auto_increment not null,
	city_name varchar(255), 
    county_id integer,
	primary key(city_id),
    constraint forkey_county foreign key(county_id) references county(county_id)
    )
    """
            )
cursor.execute(
    """
    create table peoples (
	peoples_id integer auto_increment not null,
	given_name varchar(255) default null,
	family_name varchar(255) default null,
	date_of_birth DATE default null,
	place_of_birth varchar(255) default null,
    city_id int,
    primary key(peoples_id),
    constraint forkey_city foreign key(city_id) references city(city_id)
    )
    """
            )
print("tables created")
try:
    with open('/data/people.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        id_count = cursor.lastrowid
        for row in reader:
            cursor.execute(
                ("""
                insert ignore into peoples
                (peoples_id, given_name, family_name, date_of_birth, place_of_birth) 
                values (%s, %s, %s, %s, %s)
                """)
                , (id_count, row[0], row[1], row[2], row[3])
                )
            id_count = cursor.lastrowid + 1
except IOError:
    print("Can't read peoples csv file")

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
                """
                INSERT ignore into country (country_id, country_name) values(%s, %s)
                """
                , data_country)
            cursor.execute(
                """
                INSERT ignore into county (county_id, county_name, country_id) values(%s, %s, %s)
                """
                , data_county)
            cursor.execute(
                """
                INSERT ignore into city (city_id, city_name, county_id)  values(%s, %s, %s)
                """
                , data_city)
except IOError:
    print("Could not read places csv file")

cursor.execute(
    """
    update peoples as a
    inner join city as b on a.place_of_birth = b.city_name
    set a.city_id = b.city_id
    where a.city_id is NULL
    """
    )

cursor.execute(
    """
    select a.country_name, count(*)
    from country as a 
    inner join county as b on a.country_id = b.country_id 
    inner join city as c on b.county_id = c.county_id 
    inner join peoples as d on c.city_id = d.city_id 
    group by a.country_name 
    """
    )

data = cursor.fetchall()

try:
    with open('/data/task.json', 'w') as json_file:
        rows = {}
        for x in data:
            row = {x[0] : x[1]}
            rows.update(row)
        json.dump(rows, json_file, separators=(',', ':'))
except IOError:
    print("Unable to write output in a file")

print("Data loaded")
## Close connection
mydb.commit()
cursor.close()
mydb.close()
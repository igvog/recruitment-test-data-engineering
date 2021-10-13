# Database connection
database_name = "database"
database_user = "codetest"
database_password = "swordfish"
database_charset = "utf8"

uft_commands = ['SET NAMES utf8;', 'SET CHARACTER SET utf8;', 'SET character_set_connection=utf8;']

tables = {
    "country": 
    """
    create table country (
	country_id integer auto_increment not null,
	country_name varchar(255),
	primary key(country_id)
    )
    """
    ,
    "county": 
    """
    create table county (
	county_id integer auto_increment not null,
	county_name varchar(255), 
	country_id int ,
    primary key(county_id),
    constraint forkey_country foreign key(country_id) references country(country_id)
    )
    """
    ,
    "city": 
    """
    create table city (
	city_id integer auto_increment not null,
	city_name varchar(255), 
    county_id integer,
	primary key(city_id),
    constraint forkey_county foreign key(county_id) references county(county_id)
    )
    """
    ,
    "peoples":
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
}

insert_tables = {
    "country": 
    """
        INSERT ignore into country (country_id, country_name) values(%s, %s)
    """
    ,
    "county": 
    """
        INSERT ignore into county (county_id, county_name, country_id) values(%s, %s, %s)
    """
    ,
    "city": 
    """
        INSERT ignore into city (city_id, city_name, county_id)  values(%s, %s, %s)
    """
    ,
    "peoples":
    """
        INSERT ignore into peoples
        (peoples_id, given_name, family_name, date_of_birth, place_of_birth) 
        values (%s, %s, %s, %s, %s)
    """
}

peoples_table_update = """
    update peoples as a
    inner join city as b on a.place_of_birth = b.city_name
    set a.city_id = b.city_id
    where a.city_id is NULL
    """
main_query = """
    select a.country_name, count(*)
    from country as a 
    inner join county as b on a.country_id = b.country_id 
    inner join city as c on b.county_id = c.county_id 
    inner join peoples as d on c.city_id = d.city_id 
    group by a.country_name 
    """

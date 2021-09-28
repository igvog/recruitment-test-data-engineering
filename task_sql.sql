use codetest;
drop table if exists peoples;
drop table if exists country, county, city;

create table country (
	country_id integer auto_increment not null,
	country_name varchar(255),
	primary key(country_id)
); 

create table county (
	county_id integer auto_increment not null,
	county_name varchar(255), 
	country_id int ,
    primary key(county_id),
    constraint forkey_country foreign key(country_id) references country(country_id)
);
    
    
create table city (
	city_id integer auto_increment not null,
	city_name varchar(255), 
    county_id integer,
	primary key(city_id),
    constraint forkey_county foreign key(county_id) references county(county_id)
) ;

create table peoples (
	peoples_id integer auto_increment not null,
	given_name varchar(255) default null,
	family_name varchar(255) default null,
	date_of_birth DATE default null,
	place_of_birth varchar(255) default null,
    city_id int,
    primary key(peoples_id),
    constraint forkeyk_city foreign key(city_id) references city(city_id)
) ;
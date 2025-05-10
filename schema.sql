--Strong
CREATE TABLE neighborhood(
neighborhood_name varchar(25) UNIQUE,
crime_rate numeric(5,2),
nearby_schools varchar(20),
nearby_parks varchar(20),
PRIMARY KEY(neighborhood_name)
);
CREATE TABLE "user"(
email varchar(100) UNIQUE,
first_name varchar (20),
last_name varchar (20),
PRIMARY KEY (email)
);
CREATE TABLE prospective_renter(
email varchar(100) UNIQUE,
desired_move_in_date date,
budget numeric(15,2),
PRIMARY KEY (email),
FOREIGN KEY (email) REFERENCES "user"(email) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE agent(
email varchar(100) UNIQUE,
job_title varchar(30),
real_estate_agency varchar(50),
PRIMARY KEY (email),
FOREIGN KEY (email) REFERENCES "user"(email) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE property(
property_id varchar(8),
city varchar(20),
p_state varchar(20),
description varchar(200),
price numeric(15, 2),
sq_footage int,
email varchar(100) UNIQUE,
neighborhood_name varchar(30),
PRIMARY KEY (property_id),
FOREIGN KEY (email) REFERENCES agent (email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (neighborhood_name) REFERENCES neighborhood (neighborhood_name)
);
CREATE TABLE house(
property_id varchar(8),
num_bedrooms int,
num_bathrooms int,
PRIMARY KEY (property_id)
);
CREATE TABLE com_bldgs(
property_id varchar(8),
type_of_business varchar(30),
PRIMARY KEY (property_id)
);
CREATE TABLE apartments(
property_id varchar(8),
num_bedrooms int,
num_bathrooms int,
bldg_type varchar(50),
PRIMARY KEY(property_id)
);
CREATE TABLE land(
property_id varchar(8),
soil_type varchar(20),
topography varchar(20),
zoning varchar(20),
PRIMARY KEY(property_id)
);
CREATE TABLE vacation_home(
property_id varchar(8),
num_bedrooms int,
num_bathrooms int,
PRIMARY KEY(property_id)
);
CREATE TABLE booking(
booking_id varchar(8),
booking_date date,
reward_pts_earned int,
card_number varchar(19),
start_date date,
end_date date,
email varchar(100),
property_id varchar(8),
PRIMARY KEY(booking_id),
FOREIGN KEY (email) REFERENCES "user"(email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (property_id) REFERENCES property(property_id)
);
--Multi-valued
CREATE TABLE address(
email varchar(100) REFERENCES "user" (email) ON DELETE CASCADE ON UPDATE CASCADE,
house_number varchar(5),
street varchar(20),
city varchar(20),
addr_state varchar(20),
zip_code varchar(10),
PRIMARY KEY (email, house_number, street, city, addr_state, zip_code)
);
CREATE TABLE credit_card(
email varchar (100) REFERENCES prospective_renter(email) ON DELETE CASCADE ON UPDATE CASCADE,
card_number varchar(16),
expiration_date date,
CVV varchar(3),
PRIMARY KEY (email, card_number)
);
CREATE TABLE preferred_loc(
email varchar(100) REFERENCES prospective_renter(email) ON DELETE CASCADE ON UPDATE CASCADE,
city varchar(20),
pre_state varchar(20),
priority int,
PRIMARY KEY (email, city, pre_state)
);
CREATE TABLE amenities(
property_id varchar(8) REFERENCES property(property_id),
kitchen boolean,
wifi boolean,
pool boolean,
laundry boolean,
PRIMARY KEY (property_id)
);
--Relationships
CREATE TABLE looks_at(
email varchar(100),
booking_id varchar(8),
PRIMARY KEY(email, booking_id),
FOREIGN KEY (email) REFERENCES agent(email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);
CREATE TABLE makes(
email varchar(100),
booking_id varchar(8),
PRIMARY KEY(email, booking_id),
FOREIGN KEY (email) REFERENCES prospective_renter(email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);
--Weak
CREATE TABLE reward_program(
reward_id varchar(8),
reward_pts int default 0,
enrolled boolean default false,
email varchar(100) REFERENCES prospective_renter (email) ON DELETE CASCADE ON UPDATE CASCADE
);


--register

CREATE TABLE user_auth (
    email VARCHAR(100) PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    FOREIGN KEY (email) REFERENCES "user"(email) ON DELETE CASCADE ON UPDATE CASCADE
);
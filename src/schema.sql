CREATE TABLE user_table (
	id serial PRIMARY KEY,
	state text,
	username text,
	email text
);

CREATE TABLE product_table (
	id serial PRIMARY KEY,
	name text,
	price real,
	availability boolean
);

CREATE TABLE order_table (
	id serial PRIMARY KEY
);

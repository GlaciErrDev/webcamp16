Demo
===============================


## Prerequisites 
* PostgreSQL
* Redis


`pip install -r requirements.txt`

psql template1
CREATE USER demo_user WITH PASSWORD 'demo_password';
CREATE DATABASE demo_database;
GRANT ALL PRIVILEGES ON DATABASE demo_database TO demo_user;

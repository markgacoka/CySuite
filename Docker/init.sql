CREATE DATABASE cysuite;
CREATE USER postgres WITH PASSWORD 'Dodomans@001';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE cysuite TO postgres;
-- -------------------------------------------------
-- Run this SQL script from terminal: 
--   $ mysql --user=root --password=Tarmslyng_112 < sql_init.sql
-- -------------------------------------------------

CREATE USER 'auth_user@localhost' IDENTIFIED BY 'Auth123';
-- To delete this user, run: DROP USER 'auth_user@localhost';

CREATE DATABASE auth;
-- To delete this database, run: DROP DATABASE auth;

-- To give privileges to the "auth" database
GRANT ALL PRIVILEGES on auth.* TO 'auth_user'@'localhost';

-- To give a user the same privileges as "root": 
-- GRANT ALL PRIVILEGES ON *.* TO 'tolkien'@'%';

-- To give a user privileges only to a specific table in a given db:
-- GRANT ALL PRIVILEGES ON books.authors  TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('georgio@email.com', 'Admin123');



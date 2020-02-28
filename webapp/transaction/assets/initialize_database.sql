DROP DATABASE IF EXISTS burger_builder;
CREATE DATABASE burger_builder;

USE burger_builder;

CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
    ,user_id VARCHAR(20) NOT NULL UNIQUE KEY
    ,password VARCHAR(20) NOT NULL 
);

CREATE TABLE order_details(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
    ,meat INT DEFAULT 0 NOT NULL
    ,bacon INT DEFAULT 0 NOT NULL
    ,cheese INT DEFAULT 0 NOT NULL
    ,salad INT DEFAULT 0 NOT NULL
    ,total_cost INT NOT NULL
    ,user_id INT NOT NULL
    ,FOREIGN KEY (user_id) REFERENCES users(id)
);

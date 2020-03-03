USE burger_builder;

DROP TABLE IF EXISTS order_details; 
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
    ,user_id VARCHAR(255) NOT NULL UNIQUE KEY
    ,password VARCHAR(255) NOT NULL 
);

CREATE TABLE order_details(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
    ,meat INT DEFAULT 0 NOT NULL
    ,bacon INT DEFAULT 0 NOT NULL
    ,cheese INT DEFAULT 0 NOT NULL
    ,salad INT DEFAULT 0 NOT NULL
    ,total_cost INT NOT NULL
    ,completed BOOLEAN DEFAULT false NOT NULL 
    ,user_id INT NOT NULL
    ,FOREIGN KEY (user_id) REFERENCES users(id)
);

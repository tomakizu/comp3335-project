CREATE TABLE user (
    username varchar(256) NOT NULL PRIMARY KEY,
    password varchar(256) NOT NULL,
    create_datetime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
    id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username varchar(256) NOT NULL,
    title varchar(256) NOT NULL,
    content varchar(256) NOT NULL,
    create_datetime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES user(username)
);

CREATE USER 'appuser'@'172.%' IDENTIFIED BY 'Pa$$w0rd';
GRANT INSERT, SELECT, UPDATE, DELETE ON * TO 'appuser'@'172.%';
DROP USER 'root'@'%';
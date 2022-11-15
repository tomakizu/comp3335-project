CREATE TABLE user (
    id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    create_datetime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
    id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id int(11) NOT NULL,
    title varchar(255) NOT NULL,
    content varchar(255) NOT NULL,
    create_datetime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
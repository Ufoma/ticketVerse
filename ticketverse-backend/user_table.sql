CREATE TABLE events (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    date DATE,
    time TIME,
    image_id VARCHAR(255),
    spaces_available INT,
    followers INT DEFAULT 0
);

CREATE TABLE followers (
    id INT PRIMARY KEY,
    event_id INT,
    user_id INT,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);
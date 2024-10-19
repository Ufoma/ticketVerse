CREATE TABLE events (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    image_id VARCHAR(255),
    spaces_available INT
);

CREATE TABLE tickets (
    id INT PRIMARY KEY,
    event_id INT,
    ticket_number INT,
    FOREIGN KEY (event_id) REFERENCES events(id)
);
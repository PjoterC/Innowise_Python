-- Active: 1766609622106@@0.0.0.0@5432@innowise_python_postgres
CREATE TABLE IF NOT EXISTS Rooms (
    Id INTEGER,
    name VARCHAR(50),

    PRIMARY KEY (Id)
)


CREATE TABLE IF NOT EXISTS Students (
    id INTEGER,
    birthday TIMESTAMP,
    name VARCHAR(100),
    room INT,
    sex CHAR,

    PRIMARY KEY (id),
    FOREIGN KEY (room)
    REFERENCES Rooms(id)
)


CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    photo LONGBLOB
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    status ENUM('present', 'absent'),
    FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade
);
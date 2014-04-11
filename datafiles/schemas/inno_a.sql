CREATE TABLE IF NOT EXISTS inno_a(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    sex ENUM('Male', 'Female') NOT NULL,
    birthdate TIMESTAMP
) ENGINE=innodb;

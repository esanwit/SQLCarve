DROP TABLE IF EXISTS inno_b;
CREATE TABLE IF NOT EXISTS innodb_compact2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    userlastname VARCHAR(77) ,

    email VARCHAR(100),
    sex ENUM('Male', 'Female') NOT NULL,
    interest ENUM('Male', 'Female','Wookie','Noneofyourbusiness') NOT NULL,
    birthdate TIMESTAMP,
    favedate TIMESTAMP
) ENGINE=InnoDB;
 


-- Create dynamic innodb tables
DROP TABLE IF EXISTS innodb_compact;
CREATE TABLE IF NOT EXISTS innodb_compact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    sex ENUM('Male', 'Female') NOT NULL,
    birthdate TIMESTAMP
) ENGINE=InnoDB;





 
DROP TABLE IF EXISTS innodb_redundant;
CREATE TABLE IF NOT EXISTS innodb_redundant(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    sex ENUM('Male', 'Female') NOT NULL,
    birthdate TIMESTAMP
) ENGINE=InnoDB ROW_FORMAT=REDUNDANT;


 

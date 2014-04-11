
use sku;
drop table if exists inno_com_user_example;
CREATE TABLE IF NOT EXISTS inno_com_user_example (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_admin BOOLEAN default FALSE
) ENGINE=InnoDB;

INSERT INTO inno_com_user_example(username, email, password) VALUES
  ('Esan Wit', 'Esan.Wit@os3.nl', SHA1('Password')),
  ('Leendert van Duijn', 'Leendert.vanDuijn@os3.nl', SHA1('password')),
  ('Kevin Jonkers', 'jonkers@fox-it.nl', SHA1('1234567'))
;

drop table if exists inno_red_user_example;
CREATE TABLE IF NOT EXISTS inno_red_user_example (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_admin BOOLEAN default FALSE
) ENGINE=InnoDB ROW_FORMAT=redundant;

INSERT INTO inno_red_user_example(username, email, password) VALUES
  ('Esan Wit', 'Esan.Wit@os3.nl', SHA1('Password')),
  ('Leendert van Duijn', 'Leendert.vanDuijn@os3.nl', SHA1('password')),
  ('Kevin Jonkers', 'jonkers@fox-it.nl', SHA1('1234567'))
;



drop table if exists isam_stat_user_example;
CREATE TABLE IF NOT EXISTS isam_stat_user_example (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_admin BOOLEAN default FALSE
) ENGINE=MYISAM ROW_FORMAT=FIXED;

INSERT INTO isam_stat_user_example(username, email, password) VALUES
  ('Esan Wit', 'Esan.Wit@os3.nl', SHA1('Password')),
  ('Leendert van Duijn', 'Leendert.vanDuijn@os3.nl', SHA1('password')),
  ('Kevin Jonkers', 'jonkers@fox-it.nl', SHA1('1234567'))
;


  
drop table if exists isam_dyn_user_example;
CREATE TABLE IF NOT EXISTS isam_dyn_user_example (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_admin BOOLEAN default FALSE
) ENGINE=MYISAM;

INSERT INTO isam_dyn_user_example(username, email, password) VALUES
  ('Esan Wit', 'Esan.Wit@os3.nl', SHA1('Password')),
  ('Leendert van Duijn', 'Leendert.vanDuijn@os3.nl', SHA1('password')),
  ('Kevin Jonkers', 'jonkers@fox-it.nl', SHA1('1234567'))
;


 


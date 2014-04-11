-- Create static MYISAM tables
CREATE TABLE IF NOT EXISTS myisam_static1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_update TIMESTAMP,
    created_at TIMESTAMP
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS myisam_static2 (
    text CHAR(20) NOT NULL,
    text2 CHAR(20)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS myisam_static3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type CHAR(10) NOT NULL,
    size ENUM('small', 'medium', 'large')
) ENGINE=MYISAM;

-- Create dynamic MYISAM tables
CREATE TABLE IF NOT EXISTS myisam_dynamic1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    sex ENUM('Male', 'Female') NOT NULL,
    birthdate TIMESTAMP
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS myisam_dynamic2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user INT,
    message VARCHAR(250)
) ENGINE=MYISAM;

DROP TABLE myisam_all;
CREATE TABLE IF NOT EXISTS myisam_all (
iyyyiaaaaaa CHAR(3),
date1 DATE,
aaaaiaa CHAR(3),
datetime1 DATETIME,
aaauuaa CHAR(3),
time1 TIME,
aaaaaiia CHAR(3),
timestamp1 TIMESTAMP,
aajjyaaaa CHAR(3),
year1 YEAR,
aajjggggggaaaa CHAR(3),
float1 FLOAT,
aaajhgjghaaa CHAR(3),
double1 DOUBLE,
aaaffjaaa CHAR(3),
real1 REAL,
aaajhgaaa CHAR(3),
decimal1 DECIMAL,
aaaarzzraa CHAR(3),
numeric1 NUMERIC,
aaazaraza CHAR(3),
bit1 BIT(1),
aazaaraza CHAR(3),
bit5 BIT(5),
aazazaaa CHAR(3),
bit10 BIT(10),
azaaaaa CHAR(3),
tint1 TINYINT,
aaaazzzzaa CHAR(3),
sint1 SMALLINT,
aaaaaazaaa CHAR(3),
mint1 MEDIUMINT,
aaaarrrrrraa CHAR(3),
integer1 INT,
aawwwwaaaa CHAR(3),
bint1 BIGINT,
aaaaawwwwwa CHAR(3),
enum1 ENUM("small","medium","large"),
aaaaarwerwerwea CHAR(3),
set1 SET("red","green","blue"),
aawerweraaaa CHAR(3),
char1 CHAR(20),
aaaawerrweaa CHAR(3),
varchar1 VARCHAR(20),
aaaaweraa CHAR(3),
ttext1 TINYTEXT,
aaawwaaa CHAR(3),
text1 TEXT,
aaaafaa CHAR(3),
mtext1 MEDIUMTEXT,
aaaeaaa CHAR(3),
ltext1 LONGTEXT,
aaaadaa CHAR(3),
tblob1 TINYBLOB,
aaacaaa CHAR(3),
blob1 BLOB,
aabaaaa CHAR(3),
mblob1 MEDIUMBLOB,
aaaaaaa CHAR(3),
bblob1 LONGBLOB,
aaaaaa CHAR(3) 
) engine=myisam;

CREATE TABLE IF NOT EXISTS myisam_all2 (
char2 CHAR(3),
date1 DATE,
char3 CHAR(3),
datetime1 DATETIME,
char4 CHAR(3),
time1 TIME,
char5 CHAR(3),
timestamp1 TIMESTAMP,
char6 CHAR(3),
year1 YEAR,
char7 CHAR(3),
float1 FLOAT,
char8 CHAR(3),
double1 DOUBLE,
char9 CHAR(3),
real1 REAL,
char10 CHAR(3),
decimal1 DECIMAL,
char11 CHAR(3),
numeric1 NUMERIC,
char12 CHAR(3),
bit1 BIT(1),
char13 CHAR(3),
bit5 BIT(5),
char14 CHAR(3),
bit10 BIT(10),
char15 CHAR(3),
tint1 TINYINT,
char16 CHAR(3),
sint1 SMALLINT,
char17 CHAR(3),
mint1 MEDIUMINT,
char18 CHAR(3),
integer1 INT,
char19 CHAR(3),
bint1 BIGINT,
char20 CHAR(3),
enum1 ENUM("small","medium","large"),
char21 CHAR(3),
set1 SET("red","green","blue"),
char22 CHAR(3),
char1 CHAR(20),
char23 CHAR(3),
varchar1 VARCHAR(20),
char24 CHAR(3),
ttext1 TINYTEXT,
char25 CHAR(3),
text1 TEXT,
char26 CHAR(3),
mtext1 MEDIUMTEXT,
char27 CHAR(3),
ltext1 LONGTEXT,
char28 CHAR(3),
tblob1 TINYBLOB,
char29 CHAR(3),
blob1 BLOB,
char30 CHAR(3),
mblob1 MEDIUMBLOB,
char31 CHAR(3),
bblob1 LONGBLOB
char32 CHAR(3),
) ENGINE=MYISAM;



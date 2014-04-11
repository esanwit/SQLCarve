


-- innodb_compact
 insert into innodb_compact (username, email, sex, birthdate) values ('testuser1', 'jackson@gmail.com', 'male', '1991-01-01 23:59:59'), ('testuser2', 'shadow92@gmail.com', 'male', '1992-01-01 23:59:59'), ('testuser3', 'm.jackson@gmail.com', 'male', '1984-01-01 23:59:59'), ('testuser4', 'charlotte@gmail.com', 'female', '1984-01-01 23:59:59'), ('testuser5', 'charlotte28828@gmail.com', 'female', '1984-01-01 23:59:59'), ('shadowfox22', 'shaddowf0x@gmail.com', 'male', '1993-01-01 23:59:59'), ('fox2', 'f0x@gmail.com', 'male', '1993-01-01 23:59:59'), ('fox2', 'f0x@gmail.com', 'male', '1993-01-01 23:59:59'), ('Kelinma', 'j.kleinema@gmail.com', 'male', '1999-01-01 23:59:59'), ('Mailbot', 'mailbot@hotmail.com', 'male', '1999-01-01 23:59:59'); 



-- innodb_dynamic1

insert into innodb_compact2 (username,userlastname, email, sex,tinder, birthdate, favedate) values
('testuser1','Johnson', 'jackson@gmail.com', 'male','wookie', '1995-11-11 12:12:12','1995-11-11 12:12:12');
('testuser2','Johnson', 'jackson_2@gmail.com', 'male','wookie', '1995-11-11 12:12:12','1995-11-11 12:12:12'),
('testuser3','Johnson', 'jackson_3@gmail.com', 'male','wookie', '1995-11-11 12:12:12','1995-11-11 12:12:12'),
('testuser4','Johnsonsen', 'jackson_4@gmail.com', 'male','wookie', '1995-11-11 12:12:12','1995-11-11 12:12:12');




insert into innodb_compact2 (username,email, sex,tinder, birthdate) values
('HeWhoIsNotNamed', 't.m.r@example.com', 'male','female', '1996-11-11 12:12:12');


insert into innodb_compact2 (username,userlastname, email, sex,tinder, birthdate, favedate) values
('Luke','Fowl', 'Bird@stars.tv', 'male','male', '1995-11-11 12:12:12', '1995-11-11 12:12:12'),
('Lint','Fowl', 'Dust@stars.tv', 'female','male', '1995-11-11 12:12:12', '1995-11-11 12:12:12'),
('C','F', 'd@s.tv', 'male','female', '1995-11-11 12:12:12', '1995-11-11 12:12:12'),
('Luke2','Fowl', 'Bird@stars.tv', 'male','male', '1995-11-11 12:12:12', '1995-11-11 12:12:12')
;

insert into innodb_compact2 (username, sex,tinder ) values
('NoSuchBloke', 'male','Noneofyourbusiness' );

 


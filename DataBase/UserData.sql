CREATE table User(
ID INTEGER NOT NULL unique primary key asc autoincrement,
Name TEXT unique,
Password TEXT);

create table UserSave(
ID INTEGER not null unique primary key asc autoincrement,
Save TEXT,
UserID REFERENCES User);
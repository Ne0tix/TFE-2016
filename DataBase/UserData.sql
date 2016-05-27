CREATE table User(
ID INTEGER NOT NULL unique primary key asc autoincrement,
Name TEXT unique,
Password TEXT);

create table UserSave(
ID INTEGER not null unique primary key asc autoincrement,
Save TEXT,
UserID REFERENCES User);

create table Level(
    ID integer not null unique primary key asc autoincrement,
    CurrentLevel TEXT
);

create table StaticSprite(
    ID integer not null unique primary key asc autoincrement,
    ClassName TEXT,
    Position TEXT,
    IDLevel REFERENCES Level
);

create table EntitySprite(
    ID integer not null unique primary key asc autoincrement,
    ClassName TEXT,
    Position TEXT,
    IDLevel REFERENCES Level
);

create table RessourceSprite(
    ID integer not null unique primary key asc autoincrement,
    ClassName TEXT,
    Position TEXT,
    IDLevel REFERENCES Level
);

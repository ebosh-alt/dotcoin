drop table if exists users;

create table users(
    id integer primary key,
    name varchar(200),
    username varchar(200),
    ref_link varchar(200),
    count int,
    requisites varchar(200),
    buy bool default True,
    status bool default True
);

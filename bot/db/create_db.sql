drop table if exists users;

create table users(
    id integer primary key,
    name varchar(200),
    username varchar(200),
    ref_link varchar(200),
    balance real,
    all_balance real,
    count int,
    requisites varchar(200),
    status bool default True
);

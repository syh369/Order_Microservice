DROP DATABASE if exists f22_orders;

CREATE DATABASE f22_orders;
USE f22_orders;

CREATE TABLE f22_orders.order
(
    orderid         int(8) not null unique auto_increment,
    email           varchar(64) not null,
    order_date      TIMESTAMP not null DEFAULT CURRENT_TIMESTAMP COMMENT 'order_created_date',
    total           int(8) DEFAULT 0,
    shipping_info   varchar(64) not null,
    billing_info    varchar(64) not null,
    constraint order_pk primary key (orderid)
);

CREATE TABLE f22_orders.orderline
(
    lineid      int(8) not null,
    orderid     int(8) not null,
    itemid      int(8) not null,
    price       int(8),
    amount      int(8),
    subtotal    int(8),

    constraint orderline_fk
        foreign key (orderid) references f22_orders.order(orderid)
);

INSERT INTO f22_orders.order (  email,
                                total,
                                shipping_info,
                                billing_info)
VALUES ('ys3609@columbia.edu',112,'212w','credit ending in 1234'),
       ('shenyuanhao1999@gmail.com',100,'108e','debit ending in 6156');

INSERT INTO f22_orders.orderline (lineid, orderid, itemid, price, amount, subtotal)
VALUES  (1,1,49,99,1,99),
        (2,1,23,77,2,154),
        (1,2,12,66,2,132),
        (2,2,64,11,3,33);
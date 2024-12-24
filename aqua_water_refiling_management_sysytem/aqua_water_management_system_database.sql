create database aqua_reffiling_management_system;
USE aqua_reffiling_management_system;

 CREATE TABLE customer(
  customerID INT NOT NULL,
  first_name VARCHAR(50),
  middle_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(50),
  phone_number BIGINT,
  customer_type VARCHAR(50),
  balance int,
  address VARCHAR(255),
  PRIMARY KEY(customerID)
  
);
CREATE TABLE product(
product_ID INT NOT NULL AUTO_increment,
product_name VARCHAR(255),
price_per_unit FLOAT,
stock_quantity INT,
PRIMARY KEY(product_ID)
);
CREATE TABLE delivery_person(
delivery_person_ID INT NOT NULL AUTO_increment,
person_name varchar(255),
phone_number BIGINT,
avaibility VARCHAR(255),
PRIMARY KEY(delivery_person_ID)
);
CREATE TABLE orderDetails(
orderID INT NOT NULL AUTO_increment,
PRIMARY KEY(orderID)
);
CREATE TABLE delivery(
delivery_ID INT NOT NULL AUTO_increment,
order_ID INT NOT NULL,
del_date DATETIME,
del_status varchar(255),
delivery_personID INT NOT NULL,
PRIMARY KEY(delivery_ID),
FOREIGN KEY(order_ID) references orderDetails(orderID),
FOREIGN KEY(delivery_personID) references delivery_person(delivery_person_ID)
);

CREATE TABLE payment(
payment_ID INT NOT NULL AUTO_increment,
order_id INT NOT NULL,
payment_date DATETIME,
amount_paid BIGINT,
method VARCHAR(255),
status VARCHAR(255),
PRIMARY KEY(payment_ID),
FOREIGN KEY(order_id) REFERENCES OrderDetails(orderID)
);
CREATE TABLE supplier(
supplier_ID INT NOT NULL AUTO_increment,
name VARCHAR(255),
contact_number BIGINT,
email VARCHAR(255),
address VARCHAR(255),
supplied_product_ID INT NOT NULL,
PRIMARY KEY(supplier_ID),
FOREIGN KEY(supplied_product_ID) REFERENCES product(product_ID)
);

CREATE TABLE inventory(
inventory_ID INT NOT NULL AUTO_increment,
PRIMARY KEY(inventory_ID),
product_ID INT NOT NULL,
FOREIGN KEY(product_ID) REFERENCES product(product_ID),
quantity_available FLOAT,
reorder_level INT,
last_updated DATETIME
);


ALTER TABLE orderdetails
    ADD COLUMN customerID INT NOT NULL,
    ADD COLUMN orderDate DATETIME,
    ADD COLUMN deliveryDate DATETIME,
    ADD COLUMN amount FLOAT,
    ADD COLUMN orderStatus VARCHAR(50);
    ALTER TABLE orderdetails
    ADD foreign key(customerID) references customer(customerID);
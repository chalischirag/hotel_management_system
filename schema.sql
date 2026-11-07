-- Hotel Nirvana database schema + sample data
CREATE DATABASE IF NOT EXISTS myproject;
USE myproject;

CREATE TABLE IF NOT EXISTS customer (
  id          BIGINT NOT NULL AUTO_INCREMENT,
  name        VARCHAR(50),
  address     VARCHAR(100),
  phone       VARCHAR(15),
  email       VARCHAR(80),
  id_proof    VARCHAR(20),
  id_proof_no VARCHAR(25),
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS rooms (
  id        INT NOT NULL AUTO_INCREMENT,
  room_no   INT UNIQUE,
  room_type VARCHAR(20),
  room_rent DECIMAL(10,2),
  room_bed  VARCHAR(20),
  status    VARCHAR(20) DEFAULT 'free',
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS booking (
  book_id   BIGINT NOT NULL AUTO_INCREMENT,
  room_id   INT,
  cust_id   BIGINT,
  check_in  DATE,
  check_out DATE DEFAULT NULL,
  guests    INT,
  advance   DECIMAL(10,2),
  PRIMARY KEY (book_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bill (
  bill_id   BIGINT NOT NULL AUTO_INCREMENT,
  book_id   BIGINT,
  amount    DECIMAL(10,2),
  bill_date DATE,
  gst       DECIMAL(5,2),
  st        DECIMAL(5,2),
  PRIMARY KEY (bill_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS hotel_info (
  id         INT NOT NULL AUTO_INCREMENT,
  field_name VARCHAR(30),
  value      VARCHAR(100),
  PRIMARY KEY (id)
) ENGINE=InnoDB;

INSERT INTO rooms (room_no, room_type, room_rent, room_bed, status) VALUES
(101,'AC',2500,'Single Bed','free'),(102,'AC',2500,'Single Bed','free'),
(103,'AC',2500,'Single Bed','free'),(104,'AC',2500,'Single Bed','free'),
(105,'AC',3500,'Double Bed','free'),(106,'AC',3500,'Double Bed','free'),
(107,'AC',3500,'Double Bed','free'),
(201,'Delux',4500,'Double Bed','free'),(202,'Delux',4500,'Double Bed','free'),
(203,'Delux',4500,'Double Bed','free'),
(204,'Super Delux',5500,'Double Bed','free'),(205,'Super Delux',5500,'Double Bed','free'),
(301,'Queen Delight',6500,'Double Bed','free'),(302,'Queen Delight',6500,'Double Bed','free'),
(303,'King Special',7500,'Double Bed','free'),(304,'King Special',7500,'Double Bed','free'),
(401,'Luxury Suite',10000,'Double Bed','free'),(402,'Luxury Suite',10000,'Double Bed','free'),
(403,'Luxury Suite',10000,'Double Bed','free'),
(501,'Penthouse',20000,'2 bedrooms','free'),(502,'Penthouse',20000,'2 bedrooms','free'),
(111,'Non-AC',1500,'Single Bed','free'),(112,'Non-AC',1500,'Single Bed','free'),
(110,'Non-AC',2000,'Double Bed','free'),(109,'Non-AC',2000,'Double Bed','free');

INSERT INTO hotel_info (field_name, value) VALUES
('HOTEL_NAME','HOTEL NIRVANA'),
('ADDRESS','2005, SECTOR 00, GURUGRAM HARYANA'),
('CONTACT NO.','1024-1225542, 6232636988'),
('WEBSITE','WWW.NIRVANAHOSPITALITY.COM'),
('GST','5'),
('ST','2');

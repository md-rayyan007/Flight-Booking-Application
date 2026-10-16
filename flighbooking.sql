use `csce5350_grp5_flightbooking`;

-- Step 1: Create tables with no foreign key dependencies
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY,
    admin_name VARCHAR(100),
    admin_email VARCHAR(100),
    admin_pwd VARCHAR(100)
);

CREATE TABLE Airline (
    airline_id INT PRIMARY KEY,
    name VARCHAR(100),
    seats INT
);

CREATE TABLE Cities (
    city VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Airport (
    airport_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    code VARCHAR(10)
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    loyalty_id INT
);

CREATE TABLE LoyaltyProgram (
    loyalty_id INT PRIMARY KEY,
    user_id INT,
    points INT,
    tier_level VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Staff (
    staff_id INT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50)
);

-- Step 2: Create dependent tables
CREATE TABLE Flight (
    flight_id INT PRIMARY KEY,
    arrival TIMESTAMP,
    departure TIMESTAMP,
    destination VARCHAR(100),
    source VARCHAR(100),
    airline VARCHAR(100),
    seats INT,
    duration DECIMAL(5, 2),
    price DECIMAL(10, 2),
    status VARCHAR(50),
    issue TEXT,
    last_seat INT,
    bus_seats INT,
    last_bus_seat INT,
    admin_id INT,
    airline_id INT,
    city VARCHAR(100),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
    FOREIGN KEY (airline_id) REFERENCES Airline(airline_id),
    FOREIGN KEY (city) REFERENCES Cities(city)
);

CREATE TABLE Passenger_Profile (
    passenger_id INT PRIMARY KEY,
    user_id INT,
    flight_id INT,
    mobile VARCHAR(15),
    dob DATE,
    f_name VARCHAR(50),
    m_name VARCHAR(50),
    l_name VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
);

CREATE TABLE Feedback (
    feed_id INT PRIMARY KEY,
    email VARCHAR(100),
    q1 TEXT,
    q2 TEXT,
    q3 TEXT,
    rate INT,
    passenger_id INT,
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id)
);

CREATE TABLE Payment (
	payment_id INT PRIMARY KEY auto_increment,
    card_no BIGINT,
    user_id INT,
    flight_id INT,
    expire_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
);

CREATE TABLE PwdReset (
    pwd_reset_id INT PRIMARY KEY,
    pwd_reset_email VARCHAR(100),
    pwd_reset_selector VARCHAR(255),
    pwd_reset_token TEXT,
    pwd_reset_expires TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Ticket (
    ticket_id INT PRIMARY KEY,
    passenger_id INT,
    flight_id INT,
    user_id INT,
    seat_no VARCHAR(10),
    cost DECIMAL(10, 2),
    class VARCHAR(50),
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Baggage (
    baggage_id INT PRIMARY KEY,
    passenger_id INT,
    weight DECIMAL(5, 2),
    dimensions VARCHAR(50),
    ticket_id INT,
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id),
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id)
);

CREATE TABLE Meal (
    meal_id INT PRIMARY KEY,
    meal_type VARCHAR(50),
    meal_items TEXT,
    passenger_id INT,
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id)
);

CREATE TABLE Staff_Flight (
    staff_id INT,
    flight_id INT,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
);

CREATE TABLE Airport_Flight (
    flight_id INT,
    airport_id INT,
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
    FOREIGN KEY (airport_id) REFERENCES Airport(airport_id)
);

CREATE TABLE Flight_Passenger (
    flight_id INT,
    passenger_id INT,
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id)
);

CREATE TABLE Flight_Payment (
    flight_id INT,
    payment_id INT,
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)
);

CREATE TABLE Passenger_Ticket (
    passenger_id INT,
    ticket_id INT,
    FOREIGN KEY (passenger_id) REFERENCES Passenger_Profile(passenger_id),
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id)
);


--------------------------------------------------------------------------------------------------


use `csce5350_grp5_flightbooking`;

INSERT INTO Admin (admin_id, admin_name, admin_email, admin_pwd) VALUES
(1, 'Alice Johnson', 'alice@example.com', 'password123'),
(2, 'Bob Smith', 'bob@example.com', 'adminpass1'),
(3, 'Carol Adams', 'carol@example.com', 'securepwd2'),
(4, 'David Lee', 'david@example.com', 'pass1234'),
(5, 'Eve Wilson', 'eve@example.com', 'mypass123'),
(6, 'Frank Harris', 'frank@example.com', 'adminpwd'),
(7, 'Grace Hall', 'grace@example.com', 'mypassword'),
(8, 'Hank White', 'hank@example.com', 'secure123'),
(9, 'Ivy King', 'ivy@example.com', 'mypassword1'),
(10, 'Jack Brown', 'jack@example.com', 'mypassword2');


-- Airline
INSERT INTO Airline (airline_id, name, seats) VALUES
(1, 'Air Blue', 200),
(2, 'Sky High Airlines', 150),
(3, 'Jet Stream', 180),
(4, 'Cloud Nine', 170),
(5, 'Fly Away', 220),
(6, 'Eagle Wings', 250),
(7, 'Swift Air', 130),
(8, 'Oceanic Airlines', 300),
(9, 'Vista Airlines', 160),
(10, 'Nova Jet', 140);

-- Cities
INSERT INTO Cities (city) VALUES
('New York'),
('Los Angeles'),
('Chicago'),
('Houston'),
('Phoenix'),
('Philadelphia'),
('San Antonio'),
('San Diego'),
('Dallas'),
('San Jose');


-- Airport
INSERT INTO Airport (airport_id, name, city, country, code) VALUES
(1, 'JFK International', 'New York', 'USA', 'JFK'),
(2, 'LAX International', 'Los Angeles', 'USA', 'LAX'),
(3, 'ORD International', 'Chicago', 'USA', 'ORD'),
(4, 'IAH International', 'Houston', 'USA', 'IAH'),
(5, 'PHX International', 'Phoenix', 'USA', 'PHX'),
(6, 'PHL International', 'Philadelphia', 'USA', 'PHL'),
(7, 'SAT International', 'San Antonio', 'USA', 'SAT'),
(8, 'SAN International', 'San Diego', 'USA', 'SAN'),
(9, 'DAL International', 'Dallas', 'USA', 'DAL'),
(10, 'SJC International', 'San Jose', 'USA', 'SJC');


-- Users
INSERT INTO Users (user_id, username, email, password, loyalty_id) VALUES
(1, 'alice123', 'alice@example.com', 'pass123', 1),
(2, 'bob456', 'bob@example.com', 'pass456', 2),
(3, 'bobsmith', 'bob@example.com', 'pass1234', 3),
(4, 'alicejohnson', 'alice@example.com', 'securepwd', 4),
(5, 'charliebrown', 'charlie@example.com', 'mypwd123', 5),
(6, 'davidlee', 'david@example.com', 'pwd12345', 6),
(7, 'evewilson', 'eve@example.com', 'adminpass', 7),
(8, 'frankharris', 'frank@example.com', 'userpass1', 8),
(9, 'gracehall', 'grace@example.com', 'securepass2', 9),
(10, 'ivyking', 'ivy@example.com', 'password456', 10);


-- LoyaltyProgram
INSERT INTO LoyaltyProgram (loyalty_id, user_id, points, tier_level) VALUES
(1, 1, 500, 'Silver'),
(2, 2, 1000, 'Gold'),
(3, 3, 1000, 'Gold'),
(4, 4, 1200, 'Gold'),
(5, 5, 600, 'Silver'),
(6, 6, 400, 'Silver'),
(7, 7, 600, 'Silver'),
(8, 8, 1100, 'Gold'),
(9, 9, 700, 'Silver'),
(10, 10, 1500, 'GOld');


-- Flight
INSERT INTO Flight (flight_id, arrival, departure, destination, source, airline, seats, duration, price, status, issue, last_seat, bus_seats, last_bus_seat, admin_id, airline_id, city) VALUES
(1, '2024-12-05 10:00:00', '2024-12-05 08:00:00', 'Los Angeles', 'New York', 'Air Blue', 200, 2, 300.00, 'Scheduled', NULL, 180, 20, 10, 1, 1, 'New York'),
(2, '2024-12-06 15:00:00', '2024-12-06 12:00:00', 'Chicago', 'Houston', 'Sky High Airlines', 150, 3.0, 200.00, 'Scheduled', NULL, 140, 10, 8, 2, 2, 'Houston'),
(3, '2024-12-07 09:00:00', '2024-12-07 06:00:00', 'Phoenix', 'San Diego', 'Jet Stream', 180, 3.0, 150.00, 'Scheduled', NULL, 170, 10, 9, 3, 3, 'San Diego'),
(4, '2024-12-08 18:00:00', '2024-12-08 15:00:00', 'Dallas', 'Philadelphia', 'Cloud Nine', 170, 3.0, 220.00, 'Delayed', 'Maintenance Issue', 160, 10, 7, 4, 4, 'Philadelphia'),
(5, '2024-12-09 11:00:00', '2024-12-09 09:00:00', 'San Jose', 'Chicago', 'Fly Away', 220, 2.0, 280.00, 'Scheduled', NULL, 210, 10, 5, 5, 5, 'Chicago');

-- Passenger_Profile
INSERT INTO Passenger_Profile (passenger_id, user_id, flight_id, mobile, dob, f_name, m_name, l_name) VALUES
(1, 1, 1, '1234567890', '1990-05-15', 'Alice', 'Marie', 'Brown'),
(2, 2, 2, '0987654321', '1985-08-20', 'Bob', 'John', 'Smith'),
(3, 3, 3, '3456789012', '1992-03-20', 'Bob', 'C.', 'Brown'),
(4, 4, 4, '4567890123', '1995-04-10', 'Alice', 'D.', 'Johnson'),
(5, 5, 5, '5678901234', '1988-05-25', 'Charlie', 'E.', 'Davis'),
(6, 6, 1, '6789012345', '1993-06-30', 'David', 'F.', 'Miller'),
(7, 7, 2, '7890123456', '1996-07-05', 'Eve', 'G.', 'Wilson'),
(8, 8, 3, '8901234567', '1991-08-15', 'Frank', 'H.', 'Harris'),
(9, 9, 4, '9012345678', '1994-09-20', 'Grace', 'I.', 'Hall'),
(10, 10, 5, '0123456789', '1987-10-30', 'Ivy', 'J.', 'King');


-- Feedback
INSERT INTO Feedback (feed_id, email, q1, q2, q3, rate, passenger_id) VALUES
(1, 'alice@example.com', 'Great service', 'Comfortable seats', 'On-time', 5, 1),
(2, 'bob@example.com', 'Average experience', 'Crowded', 'Delayed', 3, 2),
(3, 'bob@example.com', 'Could be better', 'Limited food', 'Delayed', 3, 3),
(4, 'alice@example.com', 'Great experience', 'Friendly crew', 'Affordable prices', 5, 4),
(5, 'charlie@example.com', 'Okay overall', 'Cramped seats', 'Long boarding', 3, 5),
(6, 'david@example.com', 'Smooth flight', 'Nice amenities', 'Quick exit', 4, 6),
(7, 'eve@example.com', 'Amazing trip', 'Helpful crew', 'Fast check-in', 5, 7),
(8, 'frank@example.com', 'Average flight', 'Basic seating', 'Short delay', 3, 8),
(9, 'grace@example.com', 'Great staff', 'Modern interiors', 'Convenient timing', 5, 9),
(10, 'ivy@example.com', 'Could improve', 'Food quality', 'Delayed takeoff', 2, 10);


-- Payment
INSERT INTO Payment (payment_id, card_no, user_id, flight_id, expire_date, amount) VALUES
(1, 4111111111111111, 1, 1, '2025-01-01', 300.00),
(2, 4222222222222222, 2, 2, '2026-02-01', 200.00),
(3, 4333333333333333, 3, 3, '2024-03-01', 150.00),
(4, 4444444444444444, 4, 4, '2027-04-01', 220.00),
(5, 4555555555555555, 5, 5, '2023-05-01', 280.00),
(6, 4666666666666666, 6, 1, '2025-06-01', 300.00),
(7, 4777777777777777, 7, 2, '2024-07-01', 200.00),
(8, 4888888888888888, 8, 3, '2023-08-01', 150.00),
(9, 4999999999999999, 9, 4, '2026-09-01', 220.00),
(10, 4000000000000000, 10, 5, '2025-10-01', 280.00);


-- PwdReset
INSERT INTO PwdReset VALUES 
(1, 'alice@example.com', 'selector123', 'token123', '2024-12-31 23:59:59', 1),
(2, 'bob@example.com', 'selector456', 'token456', '2024-11-30 23:59:59', 2);

-- Ticket
INSERT INTO Ticket (ticket_id, passenger_id, flight_id, user_id, seat_no, cost, class) VALUES
(1, 1, 1, 1, 'A1', 300.00, 'Economy'),
(2, 2, 2, 2, 'B2', 350.00, 'Business'),
(3, 3, 3, 3, 'C3', 150.00, 'Business'),
(4, 4, 4, 4, 'D4', 220.00, 'Economy'),
(5, 5, 5, 5, 'E5', 280.00, 'Business'),
(6, 6, 1, 6, 'F6', 300.00, 'Economy'),
(7, 7, 2, 7, 'G7', 200.00, 'Economy'),
(8, 8, 3, 8, 'H8', 150.00, 'Business'),
(9, 9, 4, 9, 'I9', 220.00, 'Economy'),
(10, 10, 5, 10, 'J10', 280.00, 'Business');


-- Baggage
INSERT INTO Baggage VALUES 
(1, 1, 23.50, '55x40x20', 1),
(2, 2, 30.00, '60x45x25', 2);

-- Meal
INSERT INTO Meal VALUES 
(1, 'Vegetarian', 'Rice, Salad, Juice', 1),
(2, 'Non-Vegetarian', 'Chicken, Fries, Soda', 2);

-- Staff
INSERT INTO Staff (staff_id, name, position) VALUES
(1, 'Emily Davis', 'Pilot'),
(2, 'Michael Lee', 'Cabin Crew'),
(3, 'Paul Adams', 'Cabin Crew'),
(4, 'Nina Smith', 'Cabin Crew'),
(5, 'Ethan Brown', 'Ground Staff'),
(6, 'Laura Green', 'Manager'),
(7, 'James White', 'Technician'),
(8, 'Emma Taylor', 'Cabin Crew'),
(9, 'Michael Johnson', 'Cabin Crew'),
(10, 'Sophia Martin', 'Pilot');


-- Staff_Flight
INSERT INTO Staff_Flight VALUES 
(1, 1),
(2, 2);

-- Airport_Flight
INSERT INTO Airport_Flight VALUES 
(1, 1),
(2, 2);

-- Flight_Passenger
INSERT INTO Flight_Passenger VALUES 
(1, 1),
(2, 2);

-- Flight_Payment
INSERT INTO Flight_Payment VALUES 
(1, 1),
(2, 2);

-- Passenger_Ticket
INSERT INTO Passenger_Ticket VALUES 
(1, 1),
(2, 2);

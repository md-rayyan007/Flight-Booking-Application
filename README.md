# Online Flight Booking Application

A comprehensive flight booking system built with Flask and MySQL, featuring both user and admin functionalities for managing flight reservations, staff assignments, and airline operations.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [API Routes](#api-routes)
- [Database Schema](#database-schema)
- [Features Documentation](#features-documentation)

## Project Overview

This Online Flight Booking Application is a full-featured platform that allows:
- **Users**: Search, book, and manage flight reservations
- **Administrators**: Manage flights, airlines, cities, airports, and staff assignments
- **System**: Handle payments, loyalty programs, tickets, and feedback

The application follows the MVC (Model-View-Controller) architecture using Flask blueprints for modular route management.

## Features

### User Features
- **User Registration & Authentication**
  - Secure user account creation
  - Email-based login system
  - Session management

- **Profile Management**
  - Create and update passenger profile with personal information
  - Manage contact details and date of birth
  - Profile verification before flight booking

- **Flight Booking**
  - Search available flights
  - View detailed flight information
  - Book flights with seat selection
  - Multiple class options (Business, Economy)
  - Apply loyalty discounts

- **Booking Management**
  - View booked flights
  - Cancel bookings
  - View booking history and loyalty points
  - Access ticket information

- **Account Security**
  - Change password functionality
  - Session-based authentication

### Admin Features
- **Flight Management**
  - Add new flights with complete details
  - View all flights with filtering options
  - Delete flights
  - Filter flights by source and destination
  - Manage flight status and availability

- **Airline Management**
  - View all registered airlines
  - Add new airlines
  - Manage airline information

- **Airport Management**
  - View available airports
  - Add new airports with location details

- **City Management**
  - Manage city database
  - Add new cities

- **Staff Management**
  - Assign staff to flights
  - Manage staff-flight assignments

- **Admin Authentication**
  - Secure admin login
  - Admin registration
  - Session-based admin access

## Technology Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS, JavaScript
- **Database Connector**: mysql-connector-python
- **Python Version**: 3.x

## Project Structure

```
flight_booking_system/
├── config.py                    # Database configuration
├── run.py                       # Application entry point
├── flighbooking.sql            # Database schema and sample data
├── requirements.txt            # Python dependencies
├── README.md                   # Original documentation
│
├── app/
│   ├── __init__.py             # Flask app initialization and blueprint registration
│   ├── models.py               # Database models and business logic
│   ├── user_routes.py          # User authentication and booking routes
│   ├── admin_routes.py         # Admin dashboard and management routes
│   ├── adminAuth_Routes.py     # Admin authentication routes
│   │
│   ├── static/                 # Static assets (CSS, JavaScript, images)
│   │
│   └── templates/              # HTML templates
│       ├── landing_page.html   # Homepage
│       ├── index.html          # Main page
│       ├── search.html         # Flight search page
│       ├── search_results.html # Search results display
│       ├── book.html           # Flight booking page
│       │
│       ├── user/               # User templates
│       │   ├── register.html   # User registration
│       │   ├── login.html      # User login
│       │   ├── dashboard.html  # User dashboard
│       │   ├── profile.html    # User profile management
│       │   ├── book_flight.html       # Flight booking interface
│       │   └── change_password.html   # Password change
│       │
│       └── admin/              # Admin templates
│           ├── register.html   # Admin registration
│           ├── login.html      # Admin login
│           ├── dashboard.html  # Admin dashboard
│           ├── add_flight.html # Add flight form
│           ├── add_airline.html       # Add airline form
│           ├── add_airport.html       # Add airport form
│           ├── add_city.html          # Add city form
│           ├── assign_staff.html      # Staff assignment form
│           ├── view_airlines.html     # View all airlines
│           ├── view_airports.html     # View all airports
│           └── view_cities.html       # View all cities
```

## Prerequisites

- Python 3.x installed on your system
- MySQL Server installed and running
- MySQL Workbench (optional, for easier database management)
- VS Code or any Python IDE

## Installation and Setup

### Step 1: Clone or Download the Project
```bash
# Download the entire project folder
# Extract it to your desired location
```

### Step 2: Install Python Dependencies
```bash
# Navigate to the project directory
cd c:\Users\[YourUsername]\OneDrive\Desktop\OnlineFlightBookingApp\flight_booking_system

# Install required packages
pip install -r requirements.txt

# Or manually install
pip install flask
pip install mysql-connector-python
```

### Step 3: Database Setup
1. Open MySQL Workbench or MySQL Command Line
2. Create the database:
   ```sql
   CREATE DATABASE csce5350_grp5_flightbooking;
   ```
3. Open the `flighbooking.sql` file and execute all DDL (CREATE TABLE) statements
4. Execute the sample INSERT statements to populate initial data

### Step 4: Configure Database Connection
Edit `config.py` and update with your MySQL credentials:
```python
DB_CONFIG = {
    'host': '127.0.0.1',          # Your MySQL host
    'user': 'root',               # Your MySQL username
    'password': 'root',           # Your MySQL password
    'database': 'csce5350_grp5_flightbooking'
}
```

## Running the Application

### Start the Application
```bash
# Navigate to the project directory
cd c:\Users\[YourUsername]\OneDrive\Desktop\OnlineFlightBookingApp\flight_booking_system

# Run the Flask application
python run.py
```

### Access the Application
1. Open your web browser
2. Go to: `http://127.0.0.1:5000/`
3. You'll see the landing page with options to:
   - Login/Register as a User
   - Login/Register as an Admin

## API Routes

### User Routes (`/user`)
- `GET/POST /user/register` - User registration
- `GET/POST /user/login` - User login
- `GET/POST /user/user_dashboard` - User dashboard
- `GET/POST /user/user_profile` - User profile management
- `GET/POST /user/book_flight` - Book a flight
- `GET /user/my_bookings` - View booked flights
- `GET /user/my_flights` - View flight bookings
- `GET/POST /user/cancel_booking` - Cancel a booking
- `GET /user/change_password` - Change password
- `GET /user/logout` - User logout

### Admin Routes (`/admin`)
- `GET /admin/` - Admin dashboard
- `GET/POST /admin/add_flight` - Add new flight
- `GET /admin/delete_flight/<flight_id>` - Delete flight
- `GET/POST /admin/assign_staff/<flight_id>` - Assign staff to flight
- `GET /admin/view_airlines` - View all airlines
- `GET/POST /admin/add_airline` - Add new airline
- `GET /admin/view_airports` - View all airports
- `GET/POST /admin/add_airport` - Add new airport
- `GET /admin/view_cities` - View all cities
- `GET/POST /admin/add_city` - Add new city

### Admin Auth Routes (`/admin_auth`)
- `GET/POST /admin_auth/login_admin` - Admin login
- `GET/POST /admin_auth/register_admin` - Admin registration
- `GET /admin_auth/logout_admin` - Admin logout

## Database Schema

### Core Tables

**Users**
- `user_id` (INT, PRIMARY KEY)
- `username` (VARCHAR)
- `email` (VARCHAR)
- `password` (VARCHAR)
- `loyalty_id` (INT, FOREIGN KEY)

**Admin**
- `admin_id` (INT, PRIMARY KEY)
- `admin_name` (VARCHAR)
- `admin_email` (VARCHAR)
- `admin_pwd` (VARCHAR)

**Flight**
- `flight_id` (INT, PRIMARY KEY)
- `arrival` (TIMESTAMP)
- `departure` (TIMESTAMP)
- `source` (VARCHAR)
- `destination` (VARCHAR)
- `airline` (VARCHAR)
- `seats` (INT)
- `duration` (DECIMAL)
- `price` (DECIMAL)
- `status` (VARCHAR)
- `admin_id` (INT, FOREIGN KEY)
- `airline_id` (INT, FOREIGN KEY)

**Ticket**
- `ticket_id` (INT, PRIMARY KEY)
- `passenger_id` (INT, FOREIGN KEY)
- `flight_id` (INT, FOREIGN KEY)
- `user_id` (INT, FOREIGN KEY)
- `seat_no` (VARCHAR)
- `cost` (DECIMAL)
- `class` (VARCHAR - Business, Economy)

**Passenger_Profile**
- `passenger_id` (INT, PRIMARY KEY)
- `user_id` (INT, FOREIGN KEY)
- `f_name` (VARCHAR)
- `m_name` (VARCHAR)
- `l_name` (VARCHAR)
- `dob` (DATE)
- `mobile` (VARCHAR)

**Payment**
- `payment_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `card_no` (BIGINT)
- `user_id` (INT, FOREIGN KEY)
- `flight_id` (INT, FOREIGN KEY)
- `expire_date` (DATE)
- `amount` (DECIMAL)

**LoyaltyProgram**
- `loyalty_id` (INT, PRIMARY KEY)
- `user_id` (INT, FOREIGN KEY)
- `points` (INT)
- `tier_level` (VARCHAR)

**Supporting Tables**
- `Airline` - Airline information
- `Airport` - Airport details
- `Cities` - City database
- `Staff` - Staff members
- `Feedback` - User feedback
- `Baggage` - Baggage information
- `Meal` - Meal preferences
- `Staff_Flight` - Staff-Flight assignments
- `Airport_Flight` - Airport-Flight relationships

## Features Documentation

### User Workflow

1. **Registration**
   - User creates account with unique email
   - Password stored in database (consider password hashing for production)

2. **Profile Setup**
   - Complete passenger profile with personal information
   - Required before flight booking

3. **Flight Search and Booking**
   - Search flights by source and destination
   - Select preferred flight and class
   - Choose seats
   - Process payment
   - Generate ticket

4. **Booking Management**
   - View active bookings
   - Cancel bookings if needed
   - Track loyalty points
   - Apply discounts

### Admin Workflow

1. **Authentication**
   - Admin login with credentials
   - Session management

2. **Flight Management**
   - Add new flights with complete details
   - Monitor flight status
   - Delete flights if necessary
   - View all flights with filter options

3. **Resource Management**
   - Add and manage airlines, airports, cities
   - Assign staff to flights
   - Track flight capacity and seat availability

## Security Considerations

- Session-based authentication for both users and admins
- Session timeout set to 3600 seconds (1 hour)
- Secret key: 'group5databasepr' (change in production)
- Database credentials should be protected in production environment

## Future Enhancements

- Password hashing and encryption
- Email verification for registration
- Payment gateway integration
- Advanced seat selection interface
- Email notifications for bookings
- Mobile application
- Flight rating and review system
- Advanced analytics and reporting

## Troubleshooting

### Common Issues

**"Connection refused" error**
- Ensure MySQL server is running
- Check database credentials in `config.py`
- Verify database name is correct

**"Module not found" error**
- Ensure all packages in `requirements.txt` are installed
- Use: `pip install -r requirements.txt`

**Port 5000 already in use**
- Change port in `run.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

**Database tables not created**
- Execute all DDL statements from `flighbooking.sql`
- Verify database was created successfully

## Support and Documentation

For issues or questions, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Python Documentation: https://docs.python.org/3/

---



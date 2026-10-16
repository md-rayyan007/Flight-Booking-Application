from config import init_db
from datetime import datetime

# register user
def add_user(user_id, username, email, password):
    connection = init_db()
    cursor = connection.cursor()

    query = "INSERT INTO Users (user_id, username, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, username, email, password))

    connection.commit()
    cursor.close()
    connection.close()
    
def get_user_by_email(email):
    connection = init_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Users WHERE email = %s"
    cursor.execute(query, (email,))

    user = cursor.fetchone()  # Returns None if no user is found
    cursor.close()
    connection.close()

    return user

def get_user_by_id(user_id):
    connection = init_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    user = cursor.fetchone()  # Returns None if no user is found
    cursor.close()
    connection.close()

    return user

def update_user_password(user_id, new_password):
    connection = init_db()
    cursor = connection.cursor()

    query = "UPDATE Users SET password = %s WHERE user_id = %s"
    cursor.execute(query, (new_password, user_id,))

    connection.commit()
    cursor.close()
    connection.close()

def get_admin_by_email(email):
    connection = init_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Admin WHERE admin_email = %s"
    cursor.execute(query, (email,))

    admin = cursor.fetchone()  # Returns None if no user is found
    cursor.close()
    connection.close()

    return admin

def update_user_profile(user_id, f_name, m_name, l_name, dob, mobile ):
    connection = init_db()
    cursor = connection.cursor()

    try:
        # Fetch the max passenger_id to determine the next ID
        cursor.execute("SELECT MAX(passenger_id) FROM passenger_profile")
        result = cursor.fetchall()  # Fetch all rows
        passenger_id = result[0][0] + 1 if result and result[0][0] else 1

        # Check if the user already has a passenger profile
        pax_exists = check_if_user_has_passenger_profile(user_id)

        if pax_exists:
            # Fetch existing passenger_id
            cursor.execute("SELECT passenger_id FROM passenger_profile WHERE user_id = %s", (user_id,))
            passenger_id_result = cursor.fetchall()  # Fetch all rows
            if passenger_id_result:
                passenger_id = passenger_id_result[0][0]  # Assuming one result

            # Update existing profile
            update_query = """
            UPDATE passenger_profile 
            SET passenger_id = %s, f_name = %s, m_name = %s, l_name = %s, dob = %s, mobile = %s 
            WHERE user_id = %s
            """
            cursor.execute(update_query, (passenger_id, f_name, m_name, l_name, dob, mobile, user_id))
        else:
            # Insert new profile
            insert_query = """
            INSERT INTO passenger_profile (passenger_id, user_id, mobile, dob, f_name, m_name, l_name) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (passenger_id, user_id, mobile, dob, f_name, m_name, l_name))

        # Commit the transaction
        connection.commit()

    except Exception as e:
        # Rollback on error and raise
        connection.rollback()
        print("Error in update_user_profile:", e)
        raise

    finally:
        # Always close cursor and connection
        cursor.close()
        connection.close()

    
def check_if_user_has_passenger_profile(user_id):
    connection = init_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM passenger_profile WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        print("count")
        print(result[0])
        count = result[0]  
    else:
        count = 0
    return count > 0

def get_flight_by_id(flight_id):
    connection = init_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Flight WHERE flight_id = %s"
    cursor.execute(query, (flight_id,))

    flight = cursor.fetchone()
    cursor.close()
    connection.close()

    return flight

def add_flight(flight_data):
    """
    Inserts a new flight into the database.
    """
    connection = init_db()
    cursor = connection.cursor()

    query = """
        INSERT INTO Flight (
            flight_id, arrival, departure, destination, source, airline,
            seats, duration, price, status, issue, last_seat,
            bus_seats, last_bus_seat, admin_id, airline_id, city
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            flight_data['flight_id'],
            flight_data['arrival'],
            flight_data['departure'],
            flight_data['destination'],
            flight_data['source'],
            flight_data['airline'],
            flight_data['seats'],
            flight_data['duration'],
            flight_data['price'],
            flight_data['status'],
            flight_data['issue'],
            flight_data['last_seat'],
            flight_data['bus_seats'],
            flight_data['last_bus_seat'],
            flight_data['admin_id'],
            flight_data['airline_id'],
            flight_data['city']
        ))
        connection.commit()
        print("Flight added successfully.")
    except Exception as e:
        print("Error while adding flight:", e)
        raise e
    finally:
        cursor.close()
        connection.close()

def book_flight(user_id, flight_id, seat_no, card_no, expire_date):
    connection = init_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT price, last_bus_seat FROM Flight WHERE flight_id = %s", (flight_id,))
    flight = cursor.fetchone()
    
    cursor.execute("SELECT  passenger_id FROM Passenger_Profile where user_id = %s", (user_id,) )
    passenger_id_result = cursor.fetchone()
    
    if passenger_id_result:
        passenger_id = passenger_id_result[0]
        
    cursor.execute("SELECT MAX(ticket_id) FROM Ticket")
    result = cursor.fetchone()

    # If there are no tickets yet, start with ticket_id = 1
    ticket_id = result[0] + 1 if result[0] else 1
    
    if flight:
        price = flight[0]
        if int(seat_no)<flight[1]:
            booking_class = "Business"
        else:
            booking_class = "Economy"
            
        validate_payment_details(card_no, expire_date)
        
        payment_query = """
                INSERT INTO Payment (card_no, user_id, flight_id, expire_date, amount)
                VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(payment_query, (card_no, user_id, flight_id, expire_date, price))

        
        query = "INSERT INTO Ticket (ticket_id, passenger_id, user_id, flight_id, seat_no, cost, class) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (ticket_id, passenger_id, user_id, flight_id, seat_no, price, booking_class))
        
        Update_query = """
        UPDATE Passenger_Profile 
        SET flight_id = %s
        WHERE user_id = %s and 
        passenger_id = %s
        """
        cursor.execute(Update_query, (flight_id, user_id, passenger_id))

        connection.commit()
    cursor.close()
    connection.close()



# fetch all flights  
def get_all_flights(source=None, destination=None, travel_date=None):
    conn = init_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Flight"
    
    params = []
    if source:
        query += " WHERE source = %s"
        params.append(source)
    if destination:
        query += " AND destination = %s" if source else " WHERE destination = %s"
        params.append(destination)
    if travel_date:
        query += " AND travel_date = %s" if source or destination else " WHERE travel_date = %s"
        params.append(travel_date)

    cursor.execute(query, params)
    flights_data = cursor.fetchall()
    
    return flights_data

def assign_staff_to_flight(staff_id, flight_id):
    """
    Assigns a staff member to a flight in the Staff_Flight table.
    """
    connection = init_db()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO Staff_Flight (staff_id, flight_id) VALUES (%s, %s)"
        cursor.execute(query, (staff_id, flight_id))
        connection.commit()
        print(f"Staff ID {staff_id} assigned to Flight ID {flight_id} successfully.")
    except Exception as e:
        print(f"Error while assigning staff: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# Fetch loyalty points
def get_loyalty_points(user_id):
    conn = init_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT points, tier_level FROM LoyaltyProgram WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    loyalty = cursor.fetchone()
    conn.close()
    return loyalty

# Apply discount
def apply_discount(user_id, booking_id):
    conn = init_db()
    cursor = conn.cursor()

    # Fetch current points
    cursor.execute("SELECT points FROM LoyaltyProgram WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < 100:
        conn.close()
        return False  # Insufficient points

    # Apply discount
    cursor.execute("UPDATE Ticket SET cost = cost * 0.9 WHERE ticket_id = %s", (booking_id,))
    if cursor.rowcount == 0:
        conn.close()
        return False  # Failed to update ticket

    # Deduct points
    cursor.execute("UPDATE LoyaltyProgram SET points = points - 50 WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()
    return True

# Delete a flight
def delete_flight(flight_id):
    """
    Deletes a flight from the database by its flight_id.
    Removes any associated records in related tables to satisfy foreign key constraints.
    """
    connection = init_db()
    cursor = connection.cursor()

    try:
        # Delete associated records from dependent tables
        cursor.execute("DELETE FROM Staff_Flight WHERE flight_id = %s", (flight_id,))
        cursor.execute("DELETE FROM Airport_Flight WHERE flight_id = %s", (flight_id,))
        cursor.execute("DELETE FROM Flight_Passenger WHERE flight_id = %s", (flight_id,))
        cursor.execute("DELETE FROM Flight_Payment WHERE flight_id = %s", (flight_id,))

        # Finally, delete the flight from the Flight table
        cursor.execute("DELETE FROM Flight WHERE flight_id = %s", (flight_id,))

        connection.commit()
        print(f"Flight with ID {flight_id} and all related records deleted successfully.")
    except Exception as e:
        print(f"Error while deleting flight with ID {flight_id}: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


# Function to get the booked flights for a specific user
def get_booked_flights(user_id):
    # Connect to the database
    connection = init_db()
    cursor = connection.cursor()

    # SQL query to fetch all the flights booked by the user
    query = """
    SELECT f.flight_id, f.source, f.destination, f.departure, f.arrival, f.price, t.cost, f.status, t.ticket_id
    FROM Flight f
    JOIN Ticket t ON f.flight_id = t.flight_id
    WHERE t.user_id = %s
    """

    cursor.execute(query, (user_id,))
    booked_flights = cursor.fetchall()  # Fetch all results
    
    cursor.close()
    connection.close()

    # Format the results to return them as a list of dictionaries
    flight_list = []
    for flight in booked_flights:
        flight_details = {
            'flight_id': flight[0],
            'source': flight[1],
            'destination': flight[2],
            'departure': flight[3],
            'arrival': flight[4],
            'BookedPrice': flight[5],
            'DiscountedPrice': flight[6],
            'status': flight[7],
            'ticket_id': flight[8]
        }
        flight_list.append(flight_details)

    return flight_list

def get_user_profile(user_id):
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM passenger_profile WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        
        # Ensure all rows are fetched
        result = cursor.fetchall()
        
        if result:
            return result[0]  # Assuming you need only the first row
        return None
    finally:
        # Close cursor properly
        cursor.close()
        connection.close()
        

def validate_payment_details(card_no, expire_date):
    """
    Validates the payment details, including card number and expiration date.
    """

    # Validate card number length
    if len(str(card_no)) != 16:
        raise ValueError("Invalid card number. It must be 16 digits.")

    # Validate expiration date
    expire_date_obj = datetime.strptime(expire_date, "%Y-%m-%d")
    if expire_date_obj < datetime.now():
        raise ValueError("Card has expired.")


def cancel_booked_flight(ticket_id, flight_id, user_id):
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "delete from Ticket where ticket_id = %s and flight_id = %s and user_id = %s"
        cursor.execute(query, (ticket_id,flight_id,user_id,))
        if cursor.rowcount == 0:
            connection.close()
            return False 
        connection.commit();
        return True
    finally:
        # Close cursor properly
        cursor.close()
        connection.close()


def add_airline(airline_id, name, seats):
    """
    Adds a new airline to the Airline table.
    """
    connection = init_db()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO Airline (airline_id, name, seats) VALUES (%s, %s, %s)"
        cursor.execute(query, (airline_id, name, seats))
        connection.commit()
        print(f"Airline '{name}' added successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error adding airline: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


def get_all_airlines():
    """
    Retrieves all airlines from the Airline table.
    """
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT airline_id, name, seats FROM Airline"
        cursor.execute(query)
        airlines = cursor.fetchall()
        return airlines
    except Exception as e:
        print(f"Error retrieving airlines: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def add_city(city_name):
    """
    Adds a new city to the Cities table.
    """
    connection = init_db()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO Cities (city) VALUES (%s)"
        cursor.execute(query, (city_name,))
        connection.commit()
        print(f"City '{city_name}' added successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error adding city: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


def get_all_cities():
    """
    Retrieves all cities from the Cities table.
    """
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Cities"
        cursor.execute(query)
        cities = cursor.fetchall()
        return cities
    except Exception as e:
        print(f"Error retrieving cities: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()
def add_airport(airport_id, name, city, country, code):
    """
    Adds a new airport to the Airport table.
    """
    connection = init_db()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO Airport (airport_id, name, city, country, code)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (airport_id, name, city, country, code))
        connection.commit()
        print(f"Airport '{name}' added successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error adding airport: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


def get_all_airports():
    """
    Retrieves all airports from the Airport table.
    """
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT a.airport_id, a.name AS airport_name, a.city, a.country, a.code
            FROM Airport a
        """
        cursor.execute(query)
        airports = cursor.fetchall()
        return airports
    except Exception as e:
        print(f"Error retrieving airports: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()



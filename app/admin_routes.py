from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import add_flight, get_all_flights, delete_flight, assign_staff_to_flight,get_all_airlines,get_all_cities,get_all_airports;
from config import init_db

# Create a Blueprint for Admin with the url prefix '/admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard: Display all flights
@admin_bp.route('/')
def admin_dashboard():
    admin_id = session.get('admin_id')
    if not admin_id:
        flash("Please log in first.")
        return redirect(url_for('admin_auth.login_admin'))
    source = request.args.get('source')
    destination = request.args.get('destination')

    # Fetch filtered flights or all flights if no filter is applied
    flights = get_all_flights(source, destination)
    return render_template('admin/dashboard.html', flights=flights)


@admin_bp.route('/add_flight', methods=['GET', 'POST'])
def add_flight_view():
    if request.method == 'POST':
        try:
            admin_id = session.get('admin_id')
            if not admin_id:
                flash("Please log in first.")
                return redirect(url_for('admin_auth.login_admin'))
            
            # Collect form data
            flight_data = {
                'flight_id': int(request.form['flight_id']),
                'arrival': request.form['arrival'],
                'departure': request.form['departure'],
                'destination': request.form['destination'],
                'source': request.form['source'],
                'airline': request.form['airline'],
                'seats': int(request.form['seats']),
                'duration': float(request.form['duration']),
                'price': float(request.form['price']),
                'status': request.form['status'],
                'issue': request.form.get('issue', None),  # Optional field
                'last_seat': int(request.form['last_seat']),
                'bus_seats': int(request.form['bus_seats']),
                'last_bus_seat': int(request.form['last_bus_seat']),
                'admin_id': int(request.form['admin_id']),
                'airline_id': int(request.form['airline_id']),
                'city': request.form['city']
            }

            # Call the function to add flight data to the database
            add_flight(flight_data)
            print("Form data received:", flight_data)

            flash("Flight added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('admin.add_flight_view'))
    
    # Render the add flight form for GET requests
    return render_template('admin/add_flight.html')



@admin_bp.route('/assign_staff/<int:flight_id>', methods=['GET', 'POST'])
def assign_staff_view(flight_id):
    """
    Assign staff to a flight based on the flight_id.
    """
    if request.method == 'POST':
        staff_id = int(request.form['staff_id'])
        admin_id = session.get('admin_id')
        if not admin_id:
            flash("Please log in first.")
            return redirect(url_for('admin_auth.login_admin'))
        try:
            assign_staff_to_flight(staff_id, flight_id)
            flash(f"Staff with ID {staff_id} assigned to Flight {flight_id} successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"An error occurred while assigning staff: {e}", "danger")
            return redirect(url_for('admin.assign_staff_view', flight_id=flight_id))

    # Fetch all staff for the dropdown
    staff_list = get_all_staff()
    return render_template('admin/assign_staff.html', flight_id=flight_id, staff_list=staff_list)


# Delete Flight: Allows the admin to delete a flight
@admin_bp.route('/delete_flight/<int:flight_id>', methods=['POST'])
def delete_flight_view(flight_id):
    """
    Deletes a flight from the database based on the given flight_id.
    """
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            flash("Please log in first.")
            return redirect(url_for('admin_auth.login_admin'))
        delete_flight(flight_id)
        flash(f"Flight with ID {flight_id} deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the flight: {e}", "danger")
    return redirect(url_for('admin.admin_dashboard'))


def get_all_staff():
    """
    Fetches all staff from the Staff table.
    """
    connection = init_db()
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT * FROM Staff"
        cursor.execute(query)
        staff = cursor.fetchall()
        return staff
    finally:
        cursor.close()
        connection.close() 
        

@admin_bp.route('/add_airline', methods=['GET', 'POST'])
def add_airline_view():
    """
    Allows the admin to add a new airline.
    """
    if request.method == 'POST':
        try:
            admin_id = session.get('admin_id')
            if not admin_id:
                flash("Please log in first.")
                return redirect(url_for('admin_auth.login_admin'))

            # Collect form data
            airline_id = request.form['airline_id']
            airline_name = request.form['name']
            seats = request.form['seats']

            # Add airline to the database
            connection = init_db()
            cursor = connection.cursor()
            query = "INSERT INTO Airline (airline_id, name, seats) VALUES (%s, %s, %s)"
            cursor.execute(query, (airline_id, airline_name, seats))
            connection.commit()

            flash("Airline added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"An error occurred while adding the airline: {e}", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('admin/add_airline.html')

@admin_bp.route('/add_city', methods=['GET', 'POST'])
def add_city_view():
    """
    Allows the admin to add a new city.
    """
    if request.method == 'POST':
        try:
            admin_id = session.get('admin_id')
            if not admin_id:
                flash("Please log in first.", "warning")
                return redirect(url_for('admin_auth.login_admin'))

            # Collect form data
            city_name = request.form['city']

            # Add city to the database
            connection = init_db()
            cursor = connection.cursor()
            query = "INSERT INTO Cities (city) VALUES (%s)"
            cursor.execute(query, (city_name,))
            connection.commit()

            flash("City added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))  # Redirect to the dashboard
        except Exception as e:
            flash(f"An error occurred while adding the city: {e}", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('admin/add_city.html')

@admin_bp.route('/add_airport', methods=['GET', 'POST'])

def add_airport_view():
    """
    Allows the admin to add a new airport.
    """
    connection = init_db()
    cursor = connection.cursor(dictionary=True)
    try:
        # Fetch all cities for the dropdown
        cursor.execute("SELECT city FROM Cities")
        cities = cursor.fetchall()
    except Exception as e:
        flash(f"Error fetching cities: {e}", "danger")
        cities = []
    finally:
        cursor.close()
        connection.close()

    if request.method == 'POST':
        try:
            admin_id = session.get('admin_id')
            if not admin_id:
                flash("Please log in first.")
                return redirect(url_for('admin_auth.login_admin'))

            # Collect form data
            airport_id = request.form['airport_id']
            airport_name = request.form['name']
            city = request.form['city']
            country = request.form['country']
            code = request.form['code']

            # Add airport to the database
            connection = init_db()
            cursor = connection.cursor()
            query = """
                INSERT INTO Airport (airport_id, name, city, country, code) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (airport_id, airport_name, city, country, code))
            connection.commit()

            flash("Airport added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"An error occurred while adding the airport: {e}", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('admin/add_airport.html', cities=cities)

@admin_bp.route('/view_airports')
def view_airports():
    """
    Displays all airports.
    """
    try:
        airports = get_all_airports()
        return render_template('admin/view_airports.html', airports=airports)
    except Exception as e:
        flash(f"Error retrieving airports: {e}", "danger")
        return redirect(url_for('admin.admin_dashboard'))
    
@admin_bp.route('/view_cities')
def view_cities():
    """
    Displays all cities.
    """
    try:
        cities = get_all_cities()
        return render_template('admin/view_cities.html', cities=cities)
    except Exception as e:
        flash(f"Error retrieving cities: {e}", "danger")
        return redirect(url_for('admin.admin_dashboard'))
    
@admin_bp.route('/view_airlines')
def view_airlines():
    """
    Displays all airlines.
    """
    try:
        airlines = get_all_airlines()
        return render_template('admin/view_airlines.html', airlines=airlines)
    except Exception as e:
        flash(f"Error retrieving airlines: {e}", "danger")
        return redirect(url_for('admin.admin_dashboard'))


        
        
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import add_user, check_if_user_has_passenger_profile, get_user_by_email, update_user_profile, book_flight,  apply_discount,get_all_flights, get_flight_by_id, get_user_profile, get_booked_flights, get_loyalty_points
from app.models import update_user_password, get_user_by_id, cancel_booked_flight

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash password before saving
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if email already exists
        if get_user_by_email(email):
            flash('Email is already registered!')
            return redirect(url_for('user.register'))
        
        # Add new user
        add_user(user_id, username, email, password)
        flash('Registration successful! Please log in.')
        return redirect(url_for('user.login'))
    
    return render_template('user/register.html')

# Profile Manage
@user_bp.route('/user_profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.")
        return redirect(url_for('user.login'))
    print(user_id)
    # Fetch user details from the database
    user = get_user_profile(user_id)

    # Get the 'next' parameter from the query string
    next_page = request.args.get('next')
    print("Next Page:", next_page)  # Debugging line

    if request.method == 'POST':
        f_name = request.form['f_name']
        m_name = request.form['m_name']
        l_name = request.form['l_name']
        dob = request.form['dob']
        mobile = request.form['mobile']

        update_user_profile(user_id, f_name, m_name, l_name, dob, mobile)
        flash("Profile updated successfully.")

        # Redirect to the 'next' page if provided, otherwise fallback to profile
        print("Redirecting to:", next_page or url_for('user.profile'))  # Debugging line
        return redirect(next_page or url_for('user.profile'))

    return render_template('user/profile.html', user=user)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(f"Form Data Received: {request.form}")  # Debug log
        email = request.form['email']
        password = request.form['password']
        
        # Hash password and check user credentials
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        #print(hashed_password)
        user = get_user_by_email(email)
        print(f"User fetched from DB: {user}") 
        if user and (user[3] == password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]# Store user id in session
            print(f"Logged in: session['user_id'] = {session.get('user_id')}")
            print(f"Session data after login: {session}")
            flash("Logged in successfully!")
            return redirect(url_for('user.user_dashboard'))  # Redirect to dashboard after login
        else:
            flash("Invalid login credentials!")
            return redirect(url_for('user.login'))  # Redirect back to login page
    
    return render_template('user/login.html')


# Flight Booking
@user_bp.route('/book_flight', methods=['GET', 'POST'])
def book_flight_view():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.")
        return redirect(url_for('user.login'))
    
    if not check_if_user_has_passenger_profile(user_id):
        flash("Please update your profile before booking a flight.")
        return redirect(url_for('user.profile', next=url_for('user.book_flight_view')))

    # Fetch all available flights to display in the dropdown
    flights = get_all_flights()

    if request.method == 'POST':
        flight_id = request.form['flight_id']  # Get selected flight_id
        seat_no = request.form['seat_no']
        card_no = request.form['card_no']
        expire_date = request.form['expire_date']
        book_flight(user_id, flight_id, seat_no, card_no, expire_date)  # Call booking function
        flash("Flight booked successfully!")
        return redirect(url_for('user.user_dashboard'))

    return render_template('user/book_flight.html', flights=flights)

@user_bp.route('/')
def user_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.")
        return redirect(url_for('user.login'))  # Redirect to login if user is not logged in
    
    loyalty = get_loyalty_points(user_id)  # Fetch loyalty points for the user
    if not loyalty:
        loyalty = {'points': 0, 'tier_level': 'None'}
    flights = get_booked_flights(user_id)  # Get flights booked by the user
    return render_template('user/dashboard.html', loyalty=loyalty, flights=flights)

# Booking with Loyalty Discounts: Apply discount to a booking
@user_bp.route('/apply_discount/<int:booking_id>', methods=['GET', 'POST'])
def apply_discount_view(booking_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.")
        return redirect(url_for('user.login'))

    print(f"User ID: {user_id}, Booking ID: {booking_id}")

    # Apply the discount for the booking
    if apply_discount(user_id, booking_id):
        flash("Discount applied successfully!")
    else:
        flash("Discount could not be applied. Check your loyalty points.")
    
    return redirect(url_for('user.user_dashboard'))  # Redirect to update the dashboard

@user_bp.route('/logout')
def logout_user():
    session.pop('user_id', None)
    return redirect(url_for('user.login'))

@user_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        flash("You need to log in first.", "fail")
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Fetch the user data from the database
        user = get_user_by_id(session['user_id'])  # Assume this function fetches the user by ID

        # Check current password
        if user[3] != current_password:
            flash("Current password is incorrect.", "fail")
            return redirect(url_for('user.change_password'))

        # Check if new passwords match
        if new_password != confirm_password:
            flash("New passwords do not match.", "fail")
            return redirect(url_for('user.change_password'))

        # Update the password
        
        update_user_password(session['user_id'], new_password)
        flash("Password updated successfully.", "success")
        return redirect(url_for('user.user_dashboard'))

    return render_template('user/change_password.html')

@user_bp.route('/cancel_flight/<int:booking_id>/<int:flight_id>', methods=['GET', 'POST'])
def cancel_flight(booking_id, flight_id):
    user_id = session.get('user_id')
    if  not user_id:
        flash("You need to log in first.", "fail")
        return redirect(url_for('user.login'))
    
    if(cancel_booked_flight(booking_id, flight_id, user_id)):
        flash("cancelled flight successfully!")
    else:
        flash("Flight couldn't be cancelled")
    
    return redirect(url_for('user.user_dashboard'))
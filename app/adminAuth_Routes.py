from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from config import init_db

# Blueprint for admin authentication
admin_auth_bp = Blueprint('admin_auth', __name__, url_prefix='/admin/auth')


# Admin registration
@admin_auth_bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        try:
            admin_name = request.form['admin_name']
            admin_email = request.form['admin_email']
            admin_pwd = request.form['admin_pwd']

            # Hash the password
            # hashed_pwd = generate_password_hash(admin_pwd)

            # Insert into Admin table
            connection = init_db()
            cursor = connection.cursor()
            
            cursor.execute("SELECT MAX(admin_id) FROM Admin")
            result = cursor.fetchone()

            # If there are no tickets yet, start with ticket_id = 1
            admin_id = result[0] + 1 if result[0] else 1
    
            query = """
                INSERT INTO Admin (admin_id, admin_name, admin_email, admin_pwd)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (admin_id, admin_name, admin_email, admin_pwd))
            connection.commit()

            flash("Admin registered successfully!", "success")
            return redirect(url_for('admin_auth.login_admin'))
        except Exception as e:
            flash(f"Error during registration: {e}", "fail")
        finally:
            cursor.close()
            connection.close()

    return render_template('admin/register.html')


# Admin login
@admin_auth_bp.route('/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        admin_email = request.form.get('email')
        admin_pwd = request.form.get('password')
        connection = None
        cursor = None

        try:
            # Initialize database connection
            connection = init_db()
            cursor = connection.cursor(dictionary=True)

            # Query to check admin credentials
            query = """
                SELECT * FROM Admin 
                WHERE admin_email = %s AND admin_pwd = %s
            """
            cursor.execute(query, (admin_email, admin_pwd))
            admin = cursor.fetchone()
            print(admin)

            if admin:
                session['admin_id'] = admin['admin_id']
                session['admin_name'] = admin['admin_name']
                flash("Login successful!", "success")
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash("Invalid email or password.", "danger")
                return render_template('admin/login.html')

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return render_template('admin/login.html')

        finally:
            # Ensure resources are closed properly
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # Render login page for GET request
    return render_template('admin/login.html')


# Admin logout
@admin_auth_bp.route('/logout')
def logout_admin():
    session.pop('admin_id', None)
    return redirect(url_for('admin_auth.login_admin'))

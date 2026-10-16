from flask import Flask
from app.admin_routes import admin_bp  # Importing admin routes
from app.user_routes import user_bp    # Importing user routes
from app.adminAuth_Routes import admin_auth_bp
from config import init_db

app = Flask(__name__)


app.config['SECRET_KEY'] = 'group5databasepr'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  

# Register blueprints for admin and user routes
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_auth_bp)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True)

import mysql.connector

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'flightapp',
    'password': 'Flight@123',
    'database': 'csce5350_grp5_flightbooking'
}

def init_db():
    return mysql.connector.connect(**DB_CONFIG)
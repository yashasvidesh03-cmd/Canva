from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database config (update with your credentials)
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'restaurantdb'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                   (username, email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # For simplicity, returning success message; normally return token here
    return jsonify({"message": f"Welcome back, {user['username']}!"})

# Shop Location
@app.route('/api/location', methods=['GET'])
def location():
    shop_location = {
        "address": "123 Gourmet Street, Food City, FC 45678",
        "latitude": 12.9716,
        "longitude": 77.5946
    }
    return jsonify(shop_location)

# Contact Number
@app.route('/api/contact', methods=['GET'])
def contact():
    contact_info = {
        "phone": "+91-9876543210",
        "email": "contact@the90sclub.com"
    }
    return jsonify(contact_info)

# General request endpoint directing users
@app.route('/api/request', methods=['POST'])
def user_request():
    data = request.json
    query = data.get('query', '').lower()
    
    if "sign in" in query or "login" in query:
        return jsonify({"redirect": "/login", "message": "Please go to /login for sign in."})
    elif "register" in query or "sign up" in query:
        return jsonify({"redirect": "/register", "message": "Please go to /register to create a new account."})
    elif "location" in query or "where" in query:
        return jsonify({"redirect": "/location", "message": "Here is our shop location.", "location_url": "/api/location"})
    elif "contact" in query or "phone" in query or "number" in query:
        return jsonify({"redirect": "/contact", "message": "Here is our contact information.", "contact_url": "/api/contact"})
    else:
        return jsonify({"message": "Sorry, we could not process your request. Please specify if you want to login, register, get location or contact details."})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
        

from flask import Blueprint, request, jsonify, send_from_directory
import psycopg2, bcrypt, os
from dotenv import load_dotenv

load_dotenv()
auth = Blueprint('auth', __name__)

DB_PARAMS = { #all info should be in a .env file on your local machine
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

@auth.route('/register.html')
def register_page():
    return send_from_directory('static', 'register.html')

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')

    if not all([email, password, first_name, last_name, role]):
        return jsonify({"message": "All fields are required."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT email FROM \"user\" WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"message": "Email already registered."}), 409

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        cur.execute("INSERT INTO \"user\" (email, first_name, last_name) VALUES (%s, %s, %s)",
                    (email, first_name, last_name))
        cur.execute("INSERT INTO user_auth (email, password_hash, role) VALUES (%s, %s, %s)",
                    (email, password_hash, role))
        
        if role == "agent":
            cur.execute("INSERT INTO agent (email, job_title, real_estate_agency) VALUES (%s, %s, %s)",
                        (email, '', '')) 
        elif role == "renter":
            cur.execute("INSERT INTO prospective_renter (email, desired_move_in_date, budget) VALUES (%s, %s, %s)",
                        (email, None, None)) 
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Registration successful."})
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500
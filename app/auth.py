from flask import Blueprint, session, request, jsonify, send_from_directory
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

#register-------------------------------------------------------------------------
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

#profile -------------------------------------------------------------------------------------
@auth.route('/profile.html')
def profile_page():
    return send_from_directory('static', 'profile.html')

@auth.route('/api/profile')
def get_profile():
    email = session.get('user_email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute('SELECT first_name, last_name FROM "user" WHERE email = %s', (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return jsonify({'first_name': row[0], 'last_name': row[1]})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@auth.route('/api/edit-profile', methods=['POST'])
def edit_profile():
    data = request.get_json()
    current_email = data.get('current_email')
    current_password = data.get('current_password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    new_email = data.get('new_email')
    new_password = data.get('new_password')

    if not all([current_email, current_password, first_name, last_name]):
        return jsonify({"message": "All fields except 'New Email' and 'New Password' are required."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT password_hash FROM user_auth WHERE email = %s", (current_email,))
        result = cur.fetchone()
        
        if not result or not bcrypt.checkpw(current_password.encode(), result[0].encode()):
            return jsonify({"message": "Current email or password is incorrect."}), 401

        # Update first name and last name
        cur.execute("UPDATE \"user\" SET first_name = %s, last_name = %s WHERE email = %s",
                    (first_name, last_name, current_email))

        # Update email if provided
        if new_email:
            cur.execute("UPDATE \"user\" SET email = %s WHERE email = %s", (new_email, current_email))
            cur.execute("UPDATE user_auth SET email = %s WHERE email = %s", (new_email, current_email))
            current_email = new_email

        # Update password if provided
        if new_password:
            new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cur.execute("UPDATE user_auth SET password_hash = %s WHERE email = %s", 
                        (new_password_hash, current_email))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Profile updated successfully."})
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500    
    

@auth.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return '', 204

#added for now just to give register the option to go to page (still needs to be implemented)
@auth.route('/login.html')
def login_page():
    return send_from_directory('static', 'login.html')



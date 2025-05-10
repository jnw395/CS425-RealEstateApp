from flask import Blueprint, session, request, render_template, redirect, jsonify, send_from_directory
import psycopg2, os
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
@auth.route('/register')
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

        cur.execute("INSERT INTO \"user\" (email, first_name, last_name) VALUES (%s, %s, %s)",
                    (email, first_name, last_name))
        cur.execute("INSERT INTO user_auth (email, password, role) VALUES (%s, %s, %s)",
                    (email, password, role)) 
        
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

#profile (view)---------------------------------------------------------------------------------
@auth.route('/api/view-profile')
def view_profile():
    email = session.get('user_email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute('SELECT first_name, last_name FROM "user" WHERE email = %s', (email,))
        user_row = cur.fetchone()
        if not user_row:
            return jsonify({'message': 'User not found'}), 404

        first_name, last_name = user_row

        cur.execute("""
            SELECT card_number, expiration_date
            FROM credit_card
            WHERE email = %s
        """, (email,))
        cards = [
            {'card_number': row[0], 'expiration_date': row[1]}
            for row in cur.fetchall()
        ]

        cur.execute("""
            SELECT house_number, street, city, addr_state, zip_code
            FROM address
            WHERE email = %s
        """, (email,))
        addresses = [
            {'house_number': row[0], 'street': row[1], 'city': row[2], 'addr_state': row[3], 'zip_code': row[4]}
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return jsonify({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'cards': cards,
            'addresses': addresses
        })

    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500
    
@auth.route('/view-profile')
def view_profile_page():
    return send_from_directory('static', 'view-profile.html')


#profile (edit)-------------------------------------------------------------------------------------
@auth.route('/edit-profile')
def profile_page():
    return send_from_directory('static', 'edit-profile.html')

@auth.route('/api/edit-profile')
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
    credit_cards_to_add = data.get('credit_cards')
    credit_cards_to_remove = data.get('remove_credit_cards')
    addresses_to_add = data.get('addresses')
    addresses_to_remove = data.get('remove_addresses')

    if not current_email or not current_password:
        return jsonify({"message": "Email and password are required."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT password FROM user_auth WHERE email = %s", (current_email,))
        result = cur.fetchone()
        
        if not result or result[0] != current_password: # Compare plain text passwords
            return jsonify({"message": "Incorrect email or password."}), 401

        if first_name or last_name:
            cur.execute("UPDATE \"user\" SET first_name = %s, last_name = %s WHERE email = %s",
                        (first_name, last_name, current_email))

        if new_email:
            cur.execute("UPDATE \"user\" SET email = %s WHERE email = %s", (new_email, current_email))
            cur.execute("UPDATE user_auth SET email = %s WHERE email = %s", (new_email, current_email))
            current_email = new_email

        if new_password:
            # Store the plain text password (INSECURE!)
            cur.execute("UPDATE user_auth SET password = %s WHERE email = %s", 
                        (new_password, current_email))

        if credit_cards_to_add:
            for card in credit_cards_to_add:
                cur.execute("INSERT INTO credit_cards (email, card_number, card_type, expiration_date) VALUES (%s, %s, %s, %s)",
                            (current_email, card['card_number'], card['card_type'], card['expiration_date']))

        if credit_cards_to_remove:
            for card_id in credit_cards_to_remove:
                cur.execute("DELETE FROM credit_cards WHERE card_id = %s AND email = %s", (card_id, current_email))

        if addresses_to_add:
            for address in addresses_to_add:
                cur.execute("INSERT INTO address (email, address_line, city, state, postal_code, is_billing) VALUES (%s, %s, %s, %s, %s, %s)",
                            (current_email, address['address_line'], address['city'], address['state'], address['postal_code'], address['is_billing']))

        if addresses_to_remove:
            for address_id in addresses_to_remove:
                cur.execute("SELECT is_billing FROM addresses WHERE address_id = %s AND email = %s", (address_id, current_email))
                result = cur.fetchone()
                if result and result[0] == True:
                    return jsonify({"message": "Cannot delete billing address before deleting associated credit card."}), 400
                cur.execute("DELETE FROM addresses WHERE address_id = %s AND email = %s", (address_id, current_email))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Profile updated successfully."})
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

    

@auth.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

#added for now just to give register the option to go to page (still needs to be implemented)
@auth.route('/login')
def login_page():
    return send_from_directory('static', 'login.html')

@auth.route('/api/profile/details')
def profile_details():
    email = session.get('user_email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute('SELECT first_name, last_name FROM "user" WHERE email = %s', (email,))
        name_row = cur.fetchone()

        cur.execute('SELECT card_number, cardholder_name, expiration_date FROM credit_card WHERE email = %s', (email,))
        cards = cur.fetchall()

        cur.execute('SELECT address_id, address_line FROM address WHERE email = %s', (email,))
        addresses = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            'first_name': name_row[0],
            'last_name': name_row[1],
            'email': email,
            'cards': [{'card_number': c[0], 'cardholder_name': c[1], 'expiration_date': c[2]} for c in cards],
            'addresses': [{'address_id': a[0], 'address_line': a[1]} for a in addresses]
        })
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500
    
#profile (agent)------------------------------------------------------------------------------------
@auth.route('/api/agent/edit-profile', methods=['POST'])  # Agent-specific edit profile
def agent_edit_profile():
    data = request.get_json()
    current_email = data.get('current_email')
    current_password = data.get('current_password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    new_email = data.get('new_email')
    new_password = data.get('new_password')
    job_title = data.get('job_title')        # Agent-specific field
    real_estate_agency = data.get('real_estate_agency')  # Agent-specific field

    if not current_email or not current_password:
        return jsonify({"message": "Email and password are required."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT password FROM user_auth WHERE email = %s", (current_email,))
        result = cur.fetchone()
        
        if not result or result[0] != current_password:
            return jsonify({"message": "Incorrect email or password."}), 401

        # Update common fields in "user" table
        if first_name or last_name:
            cur.execute("UPDATE \"user\" SET first_name = %s, last_name = %s WHERE email = %s",
                        (first_name, last_name, current_email))

        if new_email:
            cur.execute("UPDATE \"user\" SET email = %s WHERE email = %s", (new_email, current_email))
            cur.execute("UPDATE user_auth SET email = %s WHERE email = %s", (new_email, current_email))
            cur.execute("UPDATE agent SET email = %s WHERE email = %s",(new_email, current_email)) #update agent table
            current_email = new_email

        if new_password:
            cur.execute("UPDATE user_auth SET password = %s WHERE email = %s", 
                        (new_password, current_email))

        # Update agent-specific fields in "agent" table
        if job_title or real_estate_agency:
            cur.execute("UPDATE agent SET job_title = %s, real_estate_agency = %s WHERE email = %s",
                        (job_title, real_estate_agency, current_email))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Agent profile updated successfully."})
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    
@auth.route('/api/agent/view-profile', methods=['GET'])  # Agent-specific view profile
def agent_view_profile():
    email = request.args.get('email')  # Get email from query parameters

    if not email:
        return jsonify({"message": "Email is required."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Fetch data from "user" and "agent" tables
        cur.execute("SELECT u.email, u.first_name, u.last_name, a.job_title, a.real_estate_agency "
                    "FROM \"user\" u "
                    "JOIN agent a ON u.email = a.email "
                    "WHERE u.email = %s", (email,))
        agent_data = cur.fetchone()

        if not agent_data:
            return jsonify({"message": "Agent not found."}), 404

        # Convert the tuple to a dictionary
        agent_dict = {
            'email': agent_data[0],
            'first_name': agent_data[1],
            'last_name': agent_data[2],
            'job_title': agent_data[3],
            'real_estate_agency': agent_data[4]
        }
        
        cur.close()
        conn.close()

        return jsonify(agent_dict), 200
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    
#profile (card)------------------------------------------------------------------------
@auth.route('/api/add-card', methods=['POST'])
def add_card():
    email = session.get('user_email')
    data = request.get_json()
    card_number = data.get('card_number')
    cardholder_name = data.get('cardholder_name')
    expiration_date = data.get('expiration_date')
    billing_address_id = data.get('billing_address_id')

    if not all([card_number, cardholder_name, expiration_date]):
        return jsonify({"message": "Missing fields."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""INSERT INTO credit_card (email, card_number, cardholder_name, expiration_date, billing_address_id)
                       VALUES (%s, %s, %s, %s, %s)""", 
                    (email, card_number, cardholder_name, expiration_date, billing_address_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Card added."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@auth.route('/api/delete-card', methods=['POST'])
def delete_card():
    email = session.get('user_email')
    data = request.get_json()
    card_number = data.get('card_number')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("DELETE FROM credit_card WHERE email = %s AND card_number = %s", (email, card_number))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Card deleted."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@auth.route('/api/add-address', methods=['POST'])
def add_address():
    email = session.get('user_email')
    data = request.get_json()
    address_line = data.get('address_line')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("INSERT INTO address (email, address_line) VALUES (%s, %s)", (email, address_line))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Address added."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@auth.route('/api/delete-address', methods=['POST'])
def delete_address():
    email = session.get('user_email')
    data = request.get_json()
    address_id = data.get('address_id')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        #makes sure address isn't linked to a cc
        cur.execute("SELECT COUNT(*) FROM credit_card WHERE billing_address_id = %s", (address_id,))
        if cur.fetchone()[0] > 0:
            return jsonify({"message": "Cannot delete an address linked to a card."}), 400

        cur.execute("DELETE FROM address WHERE email = %s AND address_id = %s", (email, address_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Address deleted."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

#login -------------------------------------------------------------------------------------
@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT password, role FROM user_auth WHERE email = %s", (email,))
        result = cur.fetchone()

        if result and result[0] == password: # Compare plain text passwords (INSECURE!)
            session['user_email'] = email
            
            if result[1] == 'renter':
                return jsonify({"message": "Login successful!", "redirect_url": "/renter_dash", "role": "renter"})
            elif result[1] == 'agent':
                return jsonify({"message": "Login successful!", "redirect_url": "/agent_dash", "role": "agent"})
            else:
                return jsonify({"message": "Unknown role"}), 400
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()
#reward program -------------------------------------------------------------------------

@auth.route('/reward-program')
def reward_program_page():
    email = session.get('user_email')
    if not email:
        return redirect('/login')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT reward_pts FROM reward_program WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            #user enrolled should see pts and worth
            points = row[0]
            value = points // 100
            return render_template('reward_status.html', points=points, value=value)
        else:
            #user not enrolled so sees enroll pg
            return render_template('reward_enroll.html')

    except Exception as e:
        return f"Error: {e}", 500

@auth.route('/api/enroll-reward', methods=['POST'])
def enroll_reward():
    email = session.get('user_email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        #check if enrolled
        cur.execute("SELECT 1 FROM reward_program WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return redirect('/reward-status') 

        #enrolled with 0 pts
        cur.execute("INSERT INTO reward_program (reward_pts, email) VALUES (%s, %s)", (0, email))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/reward-status')
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

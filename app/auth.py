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
    email = session.get('email')
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

@auth.route('/api/profile', methods=['GET'])
def get_profile():
    if 'email' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    email = session['email']

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("""
            SELECT u.email, u.first_name, u.last_name, ua.role
            FROM "user" u
            JOIN user_auth ua ON u.email = ua.email
            WHERE u.email = %s
        """, (email,))
        user = cur.fetchone()

        if not user:
            return jsonify({"message": "User not found"}), 404

        cur.execute("""
            SELECT house_number, street, city, addr_state, zip_code
            FROM address
            WHERE email = %s
        """, (email,))
        addresses = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "email": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "role": user[3],
            "addresses": [
                {
                    "house_number": a[0],
                    "street": a[1],
                    "city": a[2],
                    "addr_state": a[3],
                    "zip_code": a[4]
                } for a in addresses
            ]
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@auth.route('/api/profile', methods=['POST'])
def edit_profile():
    if 'email' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    email = session['email']
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    addresses = data.get('addresses', [])

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Update name
        cur.execute("""
            UPDATE "user"
            SET first_name = %s, last_name = %s
            WHERE email = %s
        """, (first_name, last_name, email))

        # Delete old addresses
        cur.execute("DELETE FROM address WHERE email = %s", (email,))

        # Insert new addresses
        for addr in addresses:
            cur.execute("""
                INSERT INTO address (email, house_number, street, city, addr_state, zip_code)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                email,
                addr['house_number'],
                addr['street'],
                addr['city'],
                addr['addr_state'],
                addr['zip_code']
            ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Profile updated successfully"})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

    

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
    email = session.get('email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute('SELECT first_name, last_name FROM "user" WHERE email = %s', (email,))
        name_row = cur.fetchone()

        if not name_row:
            return jsonify({'message': 'User not found'}), 404

        cur.execute('SELECT card_number, expiration_date FROM credit_card WHERE email = %s', (email,))
        cards = cur.fetchall()

        cur.execute('SELECT house_number, street, city, addr_state, zip_code FROM address WHERE email = %s', (email,))
        addresses = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            'first_name': name_row[0],
            'last_name': name_row[1],
            'email': email,
            'cards': [{'card_number': c[0], 'expiration_date': c[1]} for c in cards],
            'addresses': [{'house_number': a[0], 'street': a[1], 'city': a[2], 'addr_state': a[3], 'zip_code': a[4]} for a in addresses]
        })
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500
    


@auth.route('/api/get-cards-and-addresses', methods=['GET'])
def get_cards_and_addresses():
    """
    Retrieves credit card and address information for the logged-in user
    from the database tables 'credit_card' and 'address'.
    """
    conn = None  # Initialize conn outside the try block
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()  # Use the default cursor

        email = session.get('email')
        if not email:
            if conn:
                conn.close()
            return jsonify({'error': 'User not authenticated'}), 401

        # Fetch credit card information for the user.
        cursor.execute(
            "SELECT card_number, expiration_date FROM credit_card WHERE email = %s",
            (email,)
        )
        card_data = cursor.fetchall()
        card_columns = [desc[0] for desc in cursor.description]
        cards = [dict(zip(card_columns, row)) for row in card_data]

        # Fetch address information for the user.
        cursor.execute(
            "SELECT house_number, street, city, addr_state, zip_code "
            "FROM address WHERE email = %s",
            (email,)
        )
        address_data = cursor.fetchall()
        address_columns = [desc[0] for desc in cursor.description]
        addresses = [dict(zip(address_columns, row)) for row in address_data]

        cursor.close()
        if conn:
            conn.close()

        # Format the data. Handle potential None values in expiration_date
        formatted_cards = [
            {
                'card_number': card['card_number'],
                'expiration': card.get('expiration_date').strftime('%m/%y') if card.get('expiration_date') else None
            }
            for card in cards
        ]
        formatted_addresses = [
            {
                'house_number': addr['house_number'],
                'street': addr['street'],
                'city': addr['city'],
                'addr_state': addr['addr_state'],
                'zip_code': addr['zip_code']
            }
            for addr in addresses
        ]

        return jsonify({'cards': formatted_cards, 'addresses': formatted_addresses}), 200

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Internal server error: {e}'}), 500


@auth.route('/agent/edit-profile')
def agent_edit_profile_page():
    email = session.get('email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401

    agent_data = get_agent_profile_data(email)
    if not agent_data:
        return "Agent not found.", 404

    return render_template(
        'agent_edit_profile.html',
        agent_data=agent_data
    )



    
@auth.route('/agent/view-profile')
def agent_view_profile_page():
    email = session.get('email')
    if not email:
        return jsonify({'message': 'Not logged in'}), 401

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Updated query to join "user" and "agent" tables
        cur.execute("""
            SELECT u.first_name, u.last_name, a.job_title, a.real_estate_agency
            FROM "user" u
            JOIN agent a ON u.email = a.email
            WHERE u.email = %s
        """, (email,))
        agent_data = cur.fetchone()
        cur.close()
        conn.close()

        if not agent_data:
            return "Agent not found.", 404

        # Pass agent data to the template
        return render_template('agent_profile.html', agent_data=agent_data)

    except Exception as e:
        return f"Server error: {str(e)}", 500

def get_agent_profile_data(email):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            SELECT u.email, u.first_name, u.last_name, a.job_title, a.real_estate_agency
            FROM "user" u
            JOIN agent a ON u.email = a.email
            WHERE u.email = %s
        """, (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return {
                'email': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'job_title': row[3],
                'real_estate_agency': row[4]
            }
        return None
    except Exception as e:
        print("Error fetching agent profile:", str(e))
        return None

    
#profile (card)------------------------------------------------------------------------
@auth.route('/api/add-card', methods=['POST'])
def add_card():
    email = session.get('email')
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
    email = session.get('email')
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
    email = session.get('email')
    data = request.get_json()

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO address (email, house_number, street, city, addr_state, zip_code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            email,
            data['house_number'],
            data['street'],
            data['city'],
            data['addr_state'],
            data['zip_code']
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Address added."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@auth.route('/api/delete-address', methods=['POST'])
def delete_address():
    email = session.get('email')
    data = request.get_json()
    house_number = data.get('house_number')
    street = data.get('street')
    city = data.get('city')
    addr_state = data.get('addr_state')
    zip_code = data.get('zip_code')

    if not all([house_number, street, city, addr_state, zip_code]):
        return jsonify({"message": "Error: Missing address details."}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM address
            WHERE email = %s AND house_number = %s AND street = %s AND city = %s
            AND addr_state = %s AND zip_code = %s
        """, (
            email,
            house_number,
            street,
            city,
            addr_state,
            zip_code
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Address deleted."})
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
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

        if result and result[0] == password: 
            session['email'] = email
            
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
    email = session.get('email')
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

@auth.route('/api/check-reward-enrollment')
def check_reward_enrollment():
    email = session.get('email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM reward_program WHERE email = %s", (email,))
                enrolled = cur.fetchone() is not None
                return jsonify({'enrolled': enrolled})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/enroll-status')
def enroll_status():
    email = session.get('email')
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
            points = row[0]
            value = points // 100
            return render_template('reward_status.html', points=points, value=value)
        else:
            # User not enrolled, show enrollment page
            return render_template('reward_enroll')
    except Exception as e:
        return f"Error fetching enrollment status: {e}", 500


@auth.route('/api/enroll-reward', methods=['POST'])
def enroll_reward():
    email = session.get('email')
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
            return redirect('/reward_status') 

        #enrolled with 0 pts
        cur.execute("INSERT INTO reward_program (reward_pts, email) VALUES (%s, %s)", (0, email))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/reward_status')
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500




#agent dash ------------------------------------------------------
@auth.route('/agent-dash')
def agent_dashboard():
    email = session.get('email')
    
    if not email:
        return redirect('/login')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Query the 'user' table instead of 'users'
        cur.execute("SELECT role FROM user WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[0] == 'agent':
            return render_template('agent_dashboard.html', email=email)

        else:
            return redirect('/login')

    except Exception as e:
        return f"Error: {e}", 500
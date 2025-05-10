from flask import Blueprint, render_template, request, session, jsonify, send_from_directory
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

property_bp = Blueprint('property', __name__)

DB_PARAMS = { #all info should be in a .env file on your local machine
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Renter dashboard connection
@property_bp.route('/renter_dash')
def renter_dash_page():
    return render_template('renter_dash.html')

# Agent dashboard connection
@property_bp.route('/agent_dash')
def agent_dash_page():
    return render_template('agent_dash.html')

# Route for searching
@property_bp.route('/api/search', methods=['POST'])
def search_properties():
    # Get search parameters (e.g., city, price range)
    data = request.get_json()
    city = data.get('city')
    state = data.get('state')
    price_min = data.get('price_min')
    price_max = data.get('price_max')
    property_type = data.get('property_type')
    bedrooms = data.get('bedrooms')
    
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Search for properties(filter by location and price)
        # Left join to also get num_bedrooms
        query = """
            SELECT 
                p.property_id,
                p.city,
                p.p_state,
                p.price,
                p.description,
                p.property_type,
                COALESCE(h.num_bedrooms, a.num_bedrooms, v.num_bedrooms) AS num_bedrooms
            FROM property p
            LEFT JOIN house h ON p.property_id = h.property_id
            LEFT JOIN apartments a ON p.property_id = a.property_id
            LEFT JOIN vacation_home v ON p.property_id = v.property_id
            WHERE (%s IS NULL OR p.city ILIKE %s)
              AND (%s IS NULL OR p.p_state ILIKE %s)
              AND (%s IS NULL OR p.price >= %s)
              AND (%s IS NULL OR p.price <= %s)
              AND (%s IS NULL OR p.property_type ILIKE %s)
              AND (%s IS NULL OR COALESCE(h.num_bedrooms, a.num_bedrooms, v.num_bedrooms) <= %s)
        """
        cur.execute(query, (
            city, f"%{city}%",
            state, f"%{state}%",
            price_min, price_min,
            price_max, price_max,
            property_type, f"%{property_type}%" if property_type else None,
            bedrooms, bedrooms 
        ))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = [{
            "property_id": r[0],
            "city": r[1],
            "state": r[2],
            "price": float(r[3]),
            "description": r[4],
            "property_type": r[5],
            "bedrooms": r[6]

        } for r in rows]

        return jsonify({"results": results})
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Booking--------------------------------------------------
# View booking page
@property_bp.route('/view_booking')
def view_booking_page():
    return render_template('view_booking.html')

# Make booking w/payment
@property_bp.route('/api/book', methods=['POST'])
def book_property():
    data = request.form
    property_id = data['property_id']
    start_date = data['start_date']
    end_date = data['end_date']
    credit_card_number = data['credit_card']  # The selected credit card number

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Check if the selected credit card exists
        query = "SELECT * FROM credit_card WHERE card_number = %s"
        cur.execute(query, (credit_card_number,))
        card = cur.fetchone()

        if not card:
            return jsonify({"message": "Invalid credit card selected."}), 400
        
        # Insert the booking into the bookings table
        query = """
            INSERT INTO bookings (property_id, start_date, end_date, credit_card_number)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (property_id, start_date, end_date, credit_card_number))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Booking confirmed!"}), 200
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# View booking
@property_bp.route('/view_booking')
def view_bookings():
    # Get the current user ID (assuming the user is logged in)
    renter_id = session.get('renter_id')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Fetch bookings for the logged-in renter
        cur.execute("""
            SELECT b.booking_id, p.city, p.p_state, p.price, b.start_date, b.end_date
            FROM booking b
            JOIN property p ON b.property_id = p.property_id
            WHERE b.renter_id = %s
        """, (renter_id,))
        bookings = cur.fetchall()

        cur.close()
        conn.close()

        # Display bookings
        return render_template('view_booking.html', bookings=bookings)

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@property_bp.route('/property-details/<property_id>', methods=['GET'])
def property_details(property_id):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Query to get details for a certain property
        query = """
            SELECT 
                p.property_id,
                p.city,
                p.p_state,
                p.price,
                p.description,
                p.property_type,
                COALESCE(h.num_bedrooms, a.num_bedrooms, v.num_bedrooms) AS num_bedrooms
            FROM property p
            LEFT JOIN house h ON p.property_id = h.property_id
            LEFT JOIN apartments a ON p.property_id = a.property_id
            LEFT JOIN vacation_home v ON p.property_id = v.property_id
            WHERE p.property_id = %s
        """
        cur.execute(query, (property_id,))
        row = cur.fetchone()

        if row:
            # find credit card for the respective renter
            email = session.get('user_email')  # Assuming user email is stored in session
            cur.execute("SELECT card_number, expiration_date FROM credit_card WHERE email = %s", (email,))
            credit_cards = cur.fetchall()

            property_details = {
                "property_id": row[0],
                "city": row[1],
                "state": row[2],
                "price": float(row[3]),
                "description": row[4],
                "property_type": row[5],
                "num_bedrooms": row[6]
            }
            cur.close()
            conn.close()
            return render_template('property_details.html', property=property_details, credit_cards=credit_cards)
        else:
            cur.close()
            conn.close()
            return "Property not found", 404
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


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

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Search for properties(filter by location and price)
        query = """
            SELECT property_id, city, p_state, price, description
            FROM property
            WHERE (%s IS NULL OR city ILIKE %s)
            AND (%s IS NULL OR p_state ILIKE %s)
            AND (%s IS NULL OR price >= %s)
            AND (%s IS NULL OR price <= %s)
        """
        cur.execute(query, (
            city, f"%{city}%",
            state, f"%{state}%",
            price_min, price_min,
            price_max, price_max
        ))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = [{
            "property_id": r[0],
            "city": r[1],
            "state": r[2],
            "price": float(r[3]),
            "description": r[4]
        } for r in rows]

        return jsonify({"results": results})
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Booking--------------------------------------------------
# View booking page
@property_bp.route('/view_booking')
def view_booking_page():
    return render_template('view_booking.html')

# Make booking
@property_bp.route('/api/book', methods=['POST'])
def book_property():
    data = request.get_json()
    renter_id = session.get('renter_id')  
    property_id = data.get('property_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        if not (property_id and start_date and end_date):
            return jsonify({"error": "Missing booking details."}), 400

        # Insert into bookings table
        cur.execute("""
            INSERT INTO booking (renter_id, property_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (renter_id, property_id, start_date, end_date))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Booking successful!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    

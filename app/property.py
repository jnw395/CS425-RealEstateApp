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
@property_bp.route('/renter_dash.html')
def renter_dash_page():
    return render_template('renter_dash.html')

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

        # Search for properties( filter by city and price)
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



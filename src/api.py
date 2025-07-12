from flask import Flask, request, jsonify
import time
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Simple in-memory cache to track which booking IDs have been requested before
requested_bookings = set()

def mock_tracking_process(booking_id, is_cached=False):
    """Mock the tracking process with realistic timing"""
    if is_cached:
        # Faster for cached requests (2-4 seconds)
        time.sleep(random.uniform(2, 4))
    else:
        # Slower for fresh requests (8-15 seconds)
        time.sleep(random.uniform(8, 15))
    
    # Mock voyage numbers and dates based on booking ID
    voyage_mapping = {
        "SINI25432400": ("YM MANDATE 0096W", "2025-02-28"),
    }
    
    if booking_id in voyage_mapping:
        voyage_number, arrival_date = voyage_mapping[booking_id]
    else:
        # Generate random but consistent data for unknown booking IDs
        random.seed(booking_id)  # Consistent random based on booking ID
        voyage_number = f"{random.randint(1, 999):03d}{random.choice(['W', 'E', 'N', 'S'])}"
        arrival_date = (datetime.now() + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
    
    return voyage_number, arrival_date

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/track', methods=['POST'])
def track_booking():
    """Main tracking endpoint"""
    try:
        data = request.json
        booking_id = data.get('booking_id')
        force_fresh = data.get('force_fresh', False)
        
        if not booking_id:
            return jsonify({"error": "booking_id is required"}), 400
        
        start_time = time.time()
        
        # Check if this booking ID has been requested before (simple in-memory cache)
        used_cache = booking_id in requested_bookings and not force_fresh
        
        # Mock the tracking process
        voyage_number, arrival_date = mock_tracking_process(booking_id, used_cache)
        
        # Add to requested bookings set for future cache simulation
        requested_bookings.add(booking_id)
        
        execution_time = time.time() - start_time
        
        response = {
            "success": True,
            "booking_id": booking_id,
            "voyage_number": voyage_number,
            "arrival_date": arrival_date,
            "execution_time": round(execution_time, 2),
            "used_cache": used_cache,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
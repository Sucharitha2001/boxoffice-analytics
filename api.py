from flask import Flask, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Box Office Analytics API! Visit /collections to see data."

@app.route('/collections')
def get_collections():
    conn = sqlite3.connect("collections.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie_collections ORDER BY scraped_at DESC")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "city": row[1],
            "language": row[2],
            "movie_name": row[3],
            "theater": row[4],
            "showtime": row[5],
            "seat_breakdown": json.loads(row[6]),
            "ticket_prices": json.loads(row[7]),
            "estimated_collection": row[8],
            "scraped_at": row[9]
        })

    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)

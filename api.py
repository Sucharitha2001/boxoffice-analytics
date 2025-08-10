from flask import Flask, jsonify
import sqlite3
import json

app = Flask(__name__)

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
    app.run(debug=True)

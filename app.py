from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('activity.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activity_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mouse_speed REAL,
                  typing_speed REAL,
                  quiz_score INTEGER,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    mouse_speed = data.get('mouse_speed', 0)
    typing_speed = data.get('typing_speed', 0)
    quiz_score = data.get('quiz_score', 0)

    # Store in database
    conn = sqlite3.connect('activity.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity_data (mouse_speed, typing_speed, quiz_score, timestamp) VALUES (?, ?, ?, ?)",
              (mouse_speed, typing_speed, quiz_score, datetime.now()))
    conn.commit()
    conn.close()

    # Fatigue detection logic
    if typing_speed < 15 or quiz_score < 7:
        message = "You seem a little tired... Need some break?!"
    elif typing_speed > 30 and quiz_score >= 8:
        message = "You are very active today... keep going!!"
    else:
        message = "You are doing fine, keep it up!"

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)

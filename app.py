from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'user': '********',
    'password': '*******',
    'host': '*************',
    'database': '********'
}

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    animal = request.form['animal']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votes (animal) VALUES (%s)", (animal,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204  # No content response

@app.route('/results', methods=['GET'])
def results():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT animal, COUNT(*) FROM votes GROUP BY animal")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    # Convert results to a list of dictionaries
    return jsonify([{'animal': animal, 'count': count} for animal, count in results])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

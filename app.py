def acces_compte(id,mp):
    import sqlite3
    conn = sqlite3.connect("COMPTE")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS compte (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT,
    mp TEXT,
    name TEXT,
    age INTEGER,
    );""")
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour autoriser ton frontend à appeler l'API

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    id = data.get('name', 'inconnu')
    mp = data.get('mp', 'inconnu')
    message = acces_compte(name,mp)
    return jsonify({'message': f'Bonjour, {return_message}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

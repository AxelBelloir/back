def acces_compte(demande):
    import sqlite3
    conn = sqlite3.connect("COMPTE.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS compte (
    IDKEY INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT,
    mp TEXT
    );""")
    if demande[0] == 0:
        cursor.execute("SELECT * FROM compte")
        compte = cursor.fetchall()
        index = 0
        while index < len(compte):
            if compte[index][1] == demande[1]:
                if compte[index][2] == demande[2]:
                    message = "Connexion reussi."
                    conn.commit
                    conn.close
                    return message
            index += 1
        message = "Identifiant ou mot-de-passe incorecte."
        conn.commit
        conn.close
        return message
    elif demande[0] == 1:
        cursor.execute("SELECT * FROM compte")
        compte = cursor.fetchall()
        index = 0
        out = False
        while index < len(compte):
            if demande[1] == compte[index][1]:
                out = True
                break
            index += 1
        if out == False:
            conn.commit
            conn.close
            cursor.execute("INSERT INTO compte (id,mp) VALUES (?,?)",(demande[1],demande[2]))
            return "Compte creer"
        else:
            conn.commit
            conn.close
            return "Cette identifiant est deja utilisée."
            
            
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour autoriser ton frontend à appeler l'API

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    id = data.get('name', 'inconnu')
    mp = data.get('mp', 'inconnu')
    action = data.get('action', 'inconnu')
    demande = [action,id,mp]
    return_message = acces_compte(demande)
    return jsonify({'message': f'{return_message}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

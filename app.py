def acces_compte(demande):
    import sqlite3
    conn = sqlite3.connect("COMPTE.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compte (
        IDKEY INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT,
        mp TEXT
    );""")
    
    action, identifiant, mot_de_passe = demande

    if action == 0:
        # Connexion
        cursor.execute("SELECT * FROM compte WHERE id = ? AND mp = ?", (identifiant, mot_de_passe))
        compte = cursor.fetchone()
        if compte:
            message = "Connexion réussie."
        else:
            message = "Identifiant ou mot de passe incorrect."
        conn.close()
        return message

    elif action == 1:
        # Création de compte
        cursor.execute("SELECT * FROM compte WHERE id = ?", (identifiant,))
        compte_existe = cursor.fetchone()
        
        if compte_existe:
            conn.close()
            return "Cet identifiant est déjà utilisé."
        else:
            cursor.execute("INSERT INTO compte (id, mp) VALUES (?, ?)", (identifiant, mot_de_passe))
            conn.commit()
            conn.close()
            return "Compte créé."

            
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

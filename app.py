def acces_compte(demande):
    import sqlite3
    conn = sqlite3.connect("DONNEE.db")
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
def acces_notes(demande):
    conn = sqlite3.connect("DONNEE.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        idkey INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT,
        matiere TEXT,
        note FLOAT,
        sur FLOAT,
        coef FLOAT,
        autre TEXT
    );""")
    if demande[0] == 0:
        cursor.execute("SELECT * FROM notes WHERE id = ?",(demande[1],))
        notes = cursor.fetchall()
        conn.commit()
        conn.close()
        return notes
    if demande[0] == 1:
        cursor.execute("INSERT INTO notes (id, matiere, note, sur, coef, autre) VALUES (?,?,?,?,?,?)", (demande[1],demande[2],demande[3],demande[4],demande[5],demande[6]))
        conn.commit()
        conn.close()
        return "note ajoutée."
    
        
def calcul_moyenne(notes):
    index = 0
    matieres = [
        ["Francais",], #francais
        [
            "Anglais",["CE",],["CO",],["EE",],["EOI",],["EOC",] #anglais
        ],
        [
            "Espagnole",["CE",],["CO",],["EE",],["EOI",],["EOC",] #espagnole
        ],
        ["Histoire",], #Histoire
        ["Mathematiques",], #Mathematiques
        ["Phisique",], #Phisique
        ["SVT",], #SVT
        ["Techno",], #Techno
        ["Arts",], #Arts
        ["Musique",], #Musique
        ["Sport",], #Sport
        ["Latin",], #Latin
        
    ]
    while index < len(matieres):
        index1 = 0
        while index1 < len(notes):
            if notes[index1][2] == matieres[index][0]:
                if matieres[index][0] == "Espagnole" or matieres[index][0] == "Anglais":
                    index2 = 1
                    while index2 < 4:
                        if notes[index1][5] == matieres[index][index2]:
                            matieres[index][index2].append(notes[index1])
                        index2 += 1
                else:
                    matieres[index].append(notes[index1])
            index1 += 1
        index += 1
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour autoriser ton frontend à appeler l'API
@app.route('/api/notes', methods=['POST'])
def notes():
    data = request.get_json()
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

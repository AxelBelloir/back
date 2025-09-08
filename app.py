def question(compte,demande):
    import sqlite3
    from random import randint
    conn = sqlite3.connect("DONNEE.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
        IDKEY INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        reponse TEXT
    );""")
    conn.commit()
    if demande[0] == 0:
        cursor.execute("INSERT INTO questions (question,reponse) VALUES (?,?)",(demande[1],demande[2]))
        conn.commit()
        conn.close()
        return "question ajouté"
    if demande[0] == 1:
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        questions = list(questions)
        while 0 < len(questions):
            index = randint(0,len(questions))
            question = questions[index][1]
            return jsonify({'question': f'{question}'})
            data  = request.get_json()
            reponse = data.get('reponse')
            if reponse == questions[index][2]:
                questions.remove(index)
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
    
        
def calcul_moyenne(id):
    conn = sqlite3.connect("DONNEE.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    notes = cursor.fetchall()
    index = 0
    note = 0
    coef = 0
    while index < len(notes):
        note += (notes[index][3] / notes[index][4]) * notes[index][5]
        coef += notes[index][5]
        index += 1
    moyenne = note / coef
    return moyenne

    
    
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour autoriser ton frontend à appeler l'API
@app.route('/api/notes', methods=['POST'])
def notes(id):
    data = request.get_json()
    action = data.get('action')
    acces_compte(demande)
    if action == 0:
        matiere = data.get('matiere','inconnu')
        note = float(data.get('note'))
        coef = float(data.get('coef','inconnu'))
        autre = data.get('autre','inconnu')
        sur = float(data.get('sur','inconnu'))
        demande = [1, id, matiere, note, sur, coef, autre]
        acces_notes(demande)
        moyenne = calcul_moyenne(id)
        return jsonify({'message': f'Note ajoutée.')
    return jsonify({'message': 'Action inconnue'}), 400

        
@app.route('/api/greet', methods=['POST']
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

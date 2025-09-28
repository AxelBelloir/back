
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
        if identifiant == "Zecejy39" and mot_de_passe == "Zecejy39#college#axel":
            return ["Bienvenue admin","admin"]
        cursor.execute("SELECT * FROM compte WHERE id = ? AND mp = ?", (identifiant, mot_de_passe))
        compte = cursor.fetchone()
        if compte:
            message = "Connexion réussie."
        else:
            message = ["Identifiant ou mot de passe incorrect.",identifiant]
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
            return1 = ["Compte créé.",identifiant]
            return return1
def acces_notes(demande):
    import sqlite3
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
    if not notes:
        return 0
    total_pondere = 0
    total_coef = 0
    for n in notes:
        note = n[3]
        sur = n[4]
        coef = n[5]
        if sur == 0:
            continue
        # Note normalisée sur 20, pondérée par le coef
        total_pondere += (note / sur) * 20 * coef
        total_coef += coef
    if total_coef == 0:
        return 0
    return total_pondere / total_coef

    
    
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour autoriser ton frontend à appeler l'API
@app.route('/api/notes', methods=['POST'])
@app.route('/api/notes', methods=['POST'])
def notes():
    data = request.get_json()
    action = data.get('action')

    if action == 0:
        # Ajouter une note
        id = data.get('id', 'inconnu')
        matiere = data.get('matiere', 'inconnu')
        note = float(data.get('note', 0))
        coef = float(data.get('coef', 1))
        sur = float(data.get('sur', 20))
        autre = data.get('autre', '')

        demande = [1, id, matiere, note, sur, coef, autre]
        acces_notes(demande)
        return jsonify({'message': 'Note ajoutée.'})

    elif action == 1:
        # Calculer la moyenne pour une matière
        id = data.get('id', 'inconnu')
        matiere = data.get('matiere')

        demande = [0, id]
        notes = acces_notes(demande)

        # Filtrer les notes par matière
        notes_matiere = [n for n in notes if n[2] == matiere]

        moyenne = calcul_moyenne(notes_matiere)
        return jsonify({'message': f'{round(moyenne, 2)}'})
    elif action == 2:
        id = data.get('id', 'inconnu')
        demande = [0, id]
        notes = acces_notes(demande)
        moyenne = calcul_moyenne(notes)
        return jsonify({'message': f'{round(moyenne, 2)}'})
    elif action == 3:
        id = data.get('id','inconnu')
        matiere = data.get('matiere','inconnu')
        other = data.get('other','inconnu')
        demande = [0, id]
        notes = acces_notes(demande)
        notes_matiere = [n for n in notes if n[2] == matiere]
        if other != 0:
            index = 0
            while index < other:
                index1 = 0
                notes = []
                while index1 < 4:
                    notes_matiere1 = notes_matiere[index1]
                    notes.append(notes_matiere1)
                    index1 += 1
                index += 1
        else:
            notes = [notes_matiere[0],notes_matiere[1],notes_matiere[2],notes_matiere[3],notes_matiere[4]]
        return jsonify({
    'p1': f'{notes[0]}' if len(notes) > 0 else '',
    'p2': f'{notes[1]}' if len(notes) > 1 else '',
    'p3': f'{notes[2]}' if len(notes) > 2 else '',
    'p4': f'{notes[3]}' if len(notes) > 3 else '',
    'p5': f'{notes[4]}' if len(notes) > 4 else ''
})

    else:
        return jsonify({'message': 'Action inconnue'}), 400

        
@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    id = data.get('name', 'inconnu')
    mp = data.get('mp', 'inconnu')
    action = data.get('action', 'inconnu')
    demande = [action,id,mp]
    return1 = acces_compte(demande)
    return jsonify({'value': return1[1], 'message': return1[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

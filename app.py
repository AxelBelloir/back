
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

# === PARAMÈTRES DE CONNEXION POSTGRES ===
DB_PARAMS = {
    'host': 'dpg-d3dqudb7mgec73d460g0-a',
    'dbname': 'serveur',
    'user': 'serveur_user',
    'password': 'gXsmIjafpoEtKMmreRgoUTk6CkNR57kX',  # <= remplace par le bon mot de passe
    'port': 5432
}

def get_conn():
    return psycopg2.connect(**DB_PARAMS)


def acces_compte(demande):
    conn = get_conn()
    cursor = conn.cursor()

    # Créer la table si elle n'existe pas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compte (
        IDKEY SERIAL PRIMARY KEY,
        id TEXT,
        mp TEXT
    );""")

    action, identifiant, mot_de_passe = demande

    if action == 0:
        # Connexion
        if identifiant == "Zecejy39" and mot_de_passe == "Zecejy39#college#axel":
            return ["Bienvenue admin", "admin"]

        cursor.execute("SELECT * FROM compte WHERE id = %s AND mp = %s", (identifiant, mot_de_passe))
        compte = cursor.fetchone()
        conn.close()

        if compte:
            return ["Connexion réussie.", identifiant]
        else:
            return ["Identifiant ou mot de passe incorrect.", identifiant]

    elif action == 1:
        # Création de compte
        cursor.execute("SELECT * FROM compte WHERE id = %s", (identifiant,))
        compte_existe = cursor.fetchone()

        if compte_existe:
            conn.close()
            return "Cet identifiant est déjà utilisé."
        else:
            cursor.execute("INSERT INTO compte (id, mp) VALUES (%s, %s)", (identifiant, mot_de_passe))
            conn.commit()
            conn.close()
            return ["Compte créé.", identifiant]


def acces_notes(demande):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        idkey SERIAL PRIMARY KEY,
        id TEXT,
        matiere TEXT,
        note FLOAT,
        sur FLOAT,
        coef FLOAT,
        autre TEXT
    );""")

    if demande[0] == 0:
        cursor.execute("SELECT * FROM notes WHERE id = %s", (demande[1],))
        notes = cursor.fetchall()
        conn.close()
        return notes

    elif demande[0] == 1:
        cursor.execute("""
            INSERT INTO notes (id, matiere, note, sur, coef, autre)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (demande[1], demande[2], demande[3], demande[4], demande[5], demande[6]))
        conn.commit()
        conn.close()
        return "note ajoutée."


def calcul_moyenne(notes):
    if not notes:
        return 
    total_pondere = 0
    total_coef = 0
    for n in notes:
        note = n[3]
        sur = n[4]
        coef = n[5]
        if sur == 0:
            continue
        total_pondere += (note / sur) * 20 * coef
        total_coef += coef
    if total_coef == 0:
        return 0
    return total_pondere / total_coef


# === FLASK APP ===
app = Flask(__name__)
CORS(app)

@app.route('/api/notes', methods=['POST'])
def notes():
    data = request.get_json()
    action = data.get('action')

    if action == 0:
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
        id = data.get('id', 'inconnu')
        matiere = data.get('matiere')
        demande = [0, id]
        notes = acces_notes(demande)
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
        id = data.get('id', 'inconnu')
        matiere = data.get('selectMatiere', 'inconnu')
        demande = [0, id]
        toutes_notes = acces_notes(demande)

        # Filtrer par matière
        notes = [n for n in toutes_notes if n[2] == matiere]

        # Ne garder que les 5 premières (ou moins)
        notes_liste = []
        for index in range(min(5, len(notes))):
            n = notes[index]
            formatted = f"{n[3]}/{n[4]}        ({n[5]})               {n[6]}"
            notes_liste.append(formatted)

        # Remplir les cases vides si moins de 5
        while len(notes_liste) < 5:
            notes_liste.append("Aucune note")

        return jsonify({
            'p1': notes_liste[0],
            'p2': notes_liste[1],
            'p3': notes_liste[2],
            'p4': notes_liste[3],
            'p5': notes_liste[4],
        })

    else:
        return jsonify({'message': 'Action inconnue'}), 400


@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    id = data.get('name', 'inconnu')
    mp = data.get('mp', 'inconnu')
    action = data.get('action', 'inconnu')
    demande = [action, id, mp]
    return1 = acces_compte(demande)
    return jsonify({'value': return1[1], 'message': return1[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

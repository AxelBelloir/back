
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

# === PARAMÈTRES DE CONNEXION POSTGRES (EN DUR) ===
DB_PARAMS = {
    'host': 'dpg-d3dqudb7mgec73d460g0-a',
    'dbname': 'serveur',
    'user': 'serveur_user',
    'password': 'gXsmIjafpoEtKMmreRgoUTk6CkNR57kX',
    'port': 5432
}


def get_conn():
    return psycopg2.connect(**DB_PARAMS)


# === GESTION DES COMPTES ===
def acces_compte(demande):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compte (
            IDKEY SERIAL PRIMARY KEY,
            id TEXT,
            mp TEXT
        );
    """)

    action, identifiant, mot_de_passe = demande

    if action == 0:
        if identifiant == "Zecejy39" and mot_de_passe == "Zecejy39#college#axel":
            conn.close()
            return ["Bienvenue admin", "Admin"]

        cursor.execute("SELECT * FROM compte WHERE id = %s AND mp = %s", (identifiant, mot_de_passe))
        compte = cursor.fetchone()
        conn.close()

        if compte:
            return ["Connexion réussie.", identifiant]
        else:
            return ["Identifiant ou mot de passe incorrect.", identifiant]

    elif action == 1:
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
    elif action == 2:
        cursor.execute("SELECT * FROM compte")
        return1 = cursor.fetchall()
        conn.close()
        return return1


# === GESTION DES NOTES ===
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
        );
    """)

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
        return "Note ajoutée."


def moyenne_ponderee(notes):
    total = 0
    coef_total = 0
    for note, sur, coef in notes:
        if sur == 0:
            continue
        note20 = (note / sur) * 20
        total += note20 * coef
        coef_total += coef
    return total / coef_total if coef_total else 0


def calcul_moyenne(notes):
    if not notes:
        return 0

    esp = [[] for _ in range(5)]
    ang = [[] for _ in range(5)]

    total_pondere = 0
    total_coef = 0

    for n in notes:
        note, sur, coef = n[3], n[4], n[5]
        matiere = n[2]
        autre = n[6]

        if sur == 0:
            continue

        if matiere == "Espagnole":
            if autre in ["EE", "CE", "CO", "EOC", "EOI"]:
                index = ["EE", "CE", "CO", "EOC", "EOI"].index(autre)
                esp[index].append([note, sur, coef])
        elif matiere == "Anglais":
            if autre in ["EE", "CE", "CO", "EOC", "EOI"]:
                index = ["EE", "CE", "CO", "EOC", "EOI"].index(autre)
                ang[index].append([note, sur, coef])
        else:
            total_pondere += (note / sur) * 20 * coef
            total_coef += coef
    coefsSpe = [0.25,0.25,0.25,0.12,0.13]
    index = 0
    while index < 5:
        index1 = 0
        angCoef = 0
        angNote = 0
        while index1 < len(ang[index]):
            note,sur,coef = ang[index][index1][0],ang[index][index1][1],ang[index][index1][2]
            angNote += (note / sur) * 20 * coef
            angCoef += coef
            index1 += 1
        ang[index] = (angNote / angCoef) * coefsSpe[index] if angCoef else 0
        index += 1
    index = 0
    while index < 5:
        index1 = 0
        espCoef = 0
        espNote = 0
        while index1 < len(esp[index]):
            note,sur,coef = esp[index][index1][0],esp[index][index1][1],esp[index][index1][2]
            espNote += (note / sur) * 20 * coef
            espCoef += coef
            index1 += 1
        esp[index] = (espNote / espCoef) * coefsSpe[index] if espCoef else 0
        index += 1
    total_pondere += esp[1] + esp[2] + esp[3] + esp[4] + esp[0] + ang[1] + ang[2] + ang[3] + ang[4] + ang[0]
    index = 0
    while index < 5:
        moyenneT = ang[index]
        if moyenneT != 0:
            total_coef += coefsSpe[index]
        index += 1
    index = 0
    while index < 5:
        moyenneT = esp[index]
        if moyenneT != 0:
            total_coef += coefsSpe[index]
        index += 1
    return total_pondere / total_coef if total_coef else 0


# === FLASK APP ===
app = Flask(__name__)
CORS(app)

@app.route('/api/requeteadmin', methods=['POST'])
def requeteadmin():
    data = request.get_json()
    action = data.get('action')

    if action == 0:
        action = 2
        demande = [action]
        value = acces_compte(demande)
        return jsonify({'value': value})

@app.route('/api/notes', methods=['POST'])
def notes():
    data = request.get_json()
    action = data.get('action')

    if action == 0:
        try:
            id = data.get('id')
            matiere = data.get('matiere')
            note = float(data.get('note'))
            coef = float(data.get('coef'))
            sur = float(data.get('sur'))
            autre = data.get('autre', '')
        except (TypeError, ValueError):
            return jsonify({'message': 'Valeurs invalides'}), 400

        acces_notes([1, id, matiere, note, sur, coef, autre])
        return jsonify({'message': 'Note ajoutée.'})

    elif action == 1:
        id = data.get('id')
        matiere = data.get('matiere')
        notes = [n for n in acces_notes([0, id]) if n[2] == matiere]
        moyenne = calcul_moyenne(notes)
        return jsonify({'message': f'{round(moyenne, 2)}'})

    elif action == 2:
        id = data.get('id')
        notes = acces_notes([0, id])
        moyenne = calcul_moyenne(notes)
        return jsonify({'message': f'{round(moyenne, 2)}'})

    elif action == 3:
        id = data.get('id')
        matiere = data.get('selectMatiere')
        notes = [n for n in acces_notes([0, id]) if n[2] == matiere][:5]

        notes_liste = [
            f"{n[3]}/{n[4]}        ({n[5]})               {n[6]}" for n in notes
        ]
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
    id = data.get('name', '')
    mp = data.get('mp', '')
    action = data.get('action', 0)
    retour = acces_compte([action, id, mp])

    return jsonify({'value': retour[1], 'message': retour[0]})


@app.route('/')
def index():
    return jsonify({
        'status': 'API en ligne',
        'routes': [
            '/api/greet',
            '/api/notes',
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

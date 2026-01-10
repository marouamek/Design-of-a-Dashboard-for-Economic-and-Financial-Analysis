# Creer le serveur Web Flask
from flask import Flask, render_template, request, make_response
# On importe le module "flaskext.mysql"
from flaskext.mysql import MySQL
from flask import jsonify , json
from flask import Response
import openpyxl
from io import BytesIO

app = Flask(__name__)
# On crée une instance du connecteur Flask_MySQL
mysql = MySQL()

# Configuration de la connexion MySQL
app.config["MYSQL_DATABASE_HOST"] = 'localhost'
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = 'root'
app.config["MYSQL_DATABASE_PASSWORD"] = 'pass_root'
app.config["MYSQL_DATABASE_DB"] = 'db_ipc'

# on initialise le connecteur MySQL avec les parametres de connexion
mysql.init_app(app)

#*********************************** Definition des routes d'affichage des templates ***********************************
# Route pour la page d'accueil
@app.route("/")
def index():
    # Rendre le template index.html
    return render_template("index.html")  

# Route pour la page alimentation
@app.route("/alimentation")
def alimentation():
    return render_template("alimentation.html") # Rendre le template alimentation.html

@app.route("/sante")
def sante():
    return render_template("sante.html")  # Rendre le template sante.html

@app.route("/logement")
def logement():
    return render_template("logement.html")  # Rendre le template logement.html

@app.route("/transport")
def transport():
    return render_template("transport.html")  # Rendre le template transport.html

@app.route("/export")
def export_page():
    return render_template("export.html") # Rendre le template export.html


# *********************************** Definition des routes de la page d'accueil ***********************************
# Definition des routes de la page d'accueil - 04 Cartes
@app.route('/api/cardsData', methods=['GET'])
def selectCardsData():
    # Connexion a la base de donnees
    conn = mysql.connect()
    cur = conn.cursor()
    
    # 1) Année la plus inflationniste (max variation_pourcentage dans evolution_globale)
    cur.execute("""
        SELECT annee
        FROM evolution_globale
        ORDER BY variation_pourcentage DESC
        LIMIT 1;
    """)
    row = cur.fetchone()
    annee_plus_infl = row[0] if row else None
    
    # 2) Groupe qui contribue le plus à la hausse en 2024 (on garde le calcul détaillé)
    cur.execute("""
        SELECT g.label_grp, SUM(f.variation) AS contrib
        FROM Dim_Groupe g
        JOIN Fact_IPC f ON f.id_groupe = g.id_groupe
        JOIN Dim_Annee a ON a.id_annee = f.id_annee
        WHERE a.annee = 2024
        GROUP BY g.id_groupe
        ORDER BY contrib DESC
        LIMIT 1
    """)
    groupes = cur.fetchone()[0]

    # 3) Sous-groupe avec la plus forte saisonnalité (écart‑type des variations)
    cur.execute("""
        SELECT s.label_sous_grp
        FROM Dim_Sous_Groupe s
        JOIN Fact_IPC f ON f.id_sous_groupe = s.id_sous_groupe
        JOIN Dim_Annee a ON a.id_annee = f.id_annee
        WHERE a.annee BETWEEN 2015 AND 2024
        GROUP BY s.id_sous_groupe
        ORDER BY STDDEV_SAMP(f.variation) DESC
        LIMIT 1
    """)
    saisonnalite = cur.fetchone()[0]

    # 4) Variation annuelle de l’IPC en 2024 (prise directement dans evolution_globale)
    cur.execute("""
        SELECT variation_pourcentage
        FROM evolution_globale
        WHERE annee = 2024;
    """)
    row = cur.fetchone()
    var_ipc_2024 = row[0] if row else 0

    cur.close()
    conn.close()

    # Préparer les données à retourner
    data = [
        int(annee_plus_infl) if annee_plus_infl is not None else None,
        groupes,
        saisonnalite,
        float(var_ipc_2024)
    ]
    
    # Retourner les données sous forme de JSON
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'accueil - Graphiques IPC general
@app.route('/api/ipcGeneral', methods=['GET'])
def selectIpcGeneral():
    # Connexion a la base de donnees
    conn = mysql.connect()  
    cur = conn.cursor()  

    cur.execute("""
        SELECT annee, indice_general
        FROM evolution_globale
        ORDER BY annee;
    """)

    rows = cur.fetchall() 
    cur.close()
    conn.close()
    
    labels = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]

    # Préparer les données à retourner
    data = {
        "labels": labels,
        "data": values
    }
    
    # Retourner les données sous forme de JSON
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'accueil - Graphiques Variation IPC general
@app.route('/api/varIpcGeneral', methods=['GET'])
def selectVarIpcGeneral():
    # Connexion a la base de donnees
    conn = mysql.connect()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT annee, variation_pourcentage
        FROM evolution_globale
        ORDER BY annee;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    labels = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]

    # Préparer les données à retourner
    data = {
        "labels": labels,
        "data": values
    }
    
    # Retourner les données sous forme de JSON
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'accueil - Graphiques IPC general 2024 mensuel
@app.route('/api/ipcGeneral2024', methods=['GET'])
def selectIpcGeneral2024():
    conn = mysql.connect()
    cur = conn.cursor()

    # Sélection des données de 2024 uniquement
    cur.execute("""
        SELECT Mois, IndiceGeneral 
        FROM IndiceAlimentaire
        ORDER BY FIELD(Mois, 'Janv','Févr','Mars','Avril','Mai','Juin',
        'Juillet','Août','Sept','Oct','Nov','Déc');
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    labels = [row[0] for row in rows]  # Mois
    values = [float(row[1]) for row in rows]  # Indice général

    data = {
        "labels": labels,
        "data": values
    }

    return make_response(jsonify(data), 200)

# Definition des routes de la page d'accueil - Graphiques IPC par groupe
@app.route('/api/ipcParGroupe', methods=['GET'])
def selectIpcParGroupe():
    # Connexion a la base de donnees
    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.annee,
            g.label_grp,
            ROUND(SUM(sous_grp_calc.y), 2) AS ipc_groupe
        FROM Dim_Annee a

        JOIN (
            SELECT
                f.id_annee,
                f.id_groupe,
                SUM(f.ipc * sg.poids_sous_groupe) / 1000 AS y
            FROM Fact_IPC f
            JOIN Dim_Sous_Groupe sg
                ON f.id_sous_groupe = sg.id_sous_groupe
            GROUP BY
                f.id_annee,
                f.id_groupe
        ) sous_grp_calc
            ON a.id_annee = sous_grp_calc.id_annee

        JOIN Dim_Groupe g
            ON g.id_groupe = sous_grp_calc.id_groupe

        WHERE a.annee BETWEEN 2015 AND 2024
        GROUP BY a.annee, g.label_grp
        ORDER BY a.annee, g.label_grp;
    """)

    rows = cur.fetchall()
   

    cur.close()
    conn.close()

    result = []

    current_year = None
    year_obj = None

    for row in rows:
        annee = row[0]
        label = row[1]
        ipc = float(row[2])

        if annee != current_year:
            if year_obj is not None:
                result.append(year_obj)

            year_obj = {
                "annee": annee,
                "groupes": []
            }
            current_year = annee

        year_obj["groupes"].append({
            "label": label,
            "ipc": ipc
        })

    if year_obj is not None:
        result.append(year_obj)

    return make_response(jsonify(result), 200)

# *********************************** Definition des routes des pages des groupes ***********************************

# Mapping des noms de pages aux labels de groupes dans la base de donnees
group_map = {
    "alimentation": "alimentation",
    "sante": "sante",
    "logement": "logement",
    "transport": "transport"
}

# Mapping des id_graph aux listes de sous-groupes
sous_groupe_map = {
    # Definition des sous-groupes pour la page Alimentation
    "ChartCereales": [
        "pain et cereales",
        "sucre et produits sucres",
    ],

    "ChartViandes": [
        "viande et abats de mouton",
        "viande et abats de boeuf",
        "volaille, lapin et oeuf",
        "poisson frais",
        "viandes et poissons en conserve",
        
    ],

    "ChartLegumesFruits": [
        "legumes",
        "fruits",
        "pomme de terre"
    ],

    "ChartHuilesLait": [
        "huiles et graisses",
        "lait fromage et derives",
    ],

    "ChartBoissons": [
        "boissons non alcoolisees",
        "cafe the et infusion",
    ],

    "ChartAutresAliments": [
        "autres produits alimentaires",
    ],

    # Definition des sous-groupes pour la page Logement
    "ChartEnergie": [
        "electricite et gaz",
        "combustibles",
    ],

    "ChartEau": [
        "eau potable",
    ],

    "ChartLogement": [
        "loyers et charges",
        "entretien et reparation",
    ],

    # Definition des sous-groupes pour la page Sante
    "ChartMedicament": [
        "medicaments sur ordonnance",
        "medicaments non remboursables",
    ],

    "ChartSoinsMed": [
        "appareils et materiels therapeutiques",
        "soins et services medicaux", 
    ],

    "ChartCosmetiques": [
        "biens et articles de toilette",
        "coiffure, bain et douche",
    ],

    # Definition des sous-groupes pour la page Transport
    "ChartVehicules": [
        "achat vehicules, cycles et motocycles",
        "autres depenses pour vehicules"
    ],
    "ChartEntretienVehicules": [
        "reparation et entretien de vehicules",
        "pieces detachees et accessoires vehicule"
    ],
    "ChartTransportsPublics": [
        "transports"
    ],
    "ChartTelecommunications": [
        "postes et telecommunications"
    ]
}

# Definition des routes de la page d'un groupe - Graphiques IPC Donut
@app.route('/api/ipcDonut/<string:page>', methods=['GET'])
def selectIpcDonut(page):
    # Connexion a la base de donnees
    conn = mysql.connect()
    cur = conn.cursor()

    label_groupe = group_map.get(page, None)
    if label_groupe is None:
        cur.close()
        conn.close()
        return make_response(jsonify({"error": "groupe inconnu"}), 400)

    # IPC 2024 par groupe, calcule comme dans le camembert de la page d'accueil
    cur.execute("""
        SELECT 
            g.label_grp,
            ROUND(SUM(f.ipc * sg.poids_sous_groupe) / 1000, 2) AS ipc_2024
        FROM Fact_IPC f
        JOIN Dim_Sous_Groupe sg ON f.id_sous_groupe = sg.id_sous_groupe
        JOIN Dim_Groupe g       ON g.id_groupe = f.id_groupe
        JOIN Dim_Annee a        ON a.id_annee = f.id_annee
        WHERE a.annee = 2024
        GROUP BY g.label_grp;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    ipc_groupe = 0.0
    ipc_autres = 0.0
    for label, ipc in rows:
        v = float(ipc or 0)
        if label == label_groupe:
            ipc_groupe = v
        else:
            ipc_autres += v

    result = {
        "labels": [label_groupe, "Autres groupes"],
        "data": [ipc_groupe, ipc_autres]
    }
    return make_response(jsonify(result), 200)

# Definition des routes de la page d'un groupe - Graphiques 3 sous-groupes les plus inflationnistes
@app.route('/api/top3Inflation/<string:page>', methods=['GET'])
def selectTop3Inflation(page):
    # Connexion a la base de donnees
    conn = mysql.connect()
    cur = conn.cursor()

    label_groupe = group_map.get(page, None)
    if label_groupe is None:
        cur.close()
        conn.close()
        return make_response(jsonify({"error": "groupe inconnu"}), 400)

    cur.execute("""
        SELECT sg.label_sous_grp, SUM(f.variation) AS variation
        FROM Fact_IPC f
        JOIN Dim_Sous_Groupe sg ON f.id_sous_groupe = sg.id_sous_groupe
        JOIN Dim_Groupe g ON sg.id_groupe = g.id_groupe
        JOIN Dim_Annee a ON f.id_annee = a.id_annee
        WHERE g.label_grp = %s
          AND a.annee = 2024
        GROUP BY sg.id_sous_groupe
        ORDER BY variation DESC
        LIMIT 3;
    """, (label_groupe,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [{"label": r[0], "variation": float(r[1])} for r in rows]
    return make_response(jsonify(result), 200)

# Definition des routes de la page d'un groupe - Graphiques IPC par annee
@app.route('/api/ipc/<string:page>/', methods=['GET'])
def selectIpc(page):
    conn = mysql.connect()
    cur = conn.cursor()

    label_groupe = group_map.get(page, None)
    if label_groupe is None:
        cur.close()
        conn.close()
        return make_response(jsonify({"error": "groupe inconnu"}), 400)

    cur.execute("""
        SELECT 
    a.annee,
    ROUND(
        SUM(f.ipc * sg.poids_sous_groupe) / SUM(sg.poids_sous_groupe),
        2
    ) AS ipc_groupe
    FROM Fact_IPC f
    JOIN Dim_Annee a ON a.id_annee = f.id_annee
    JOIN Dim_Sous_Groupe sg ON sg.id_sous_groupe = f.id_sous_groupe
    JOIN Dim_Groupe g ON g.id_groupe = sg.id_groupe
    WHERE g.label_grp = %s
    AND a.annee BETWEEN 2015 AND 2024
    GROUP BY a.annee
    ORDER BY a.annee;
    """, (label_groupe,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    labels = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]

    data = {"labels": labels, "data": values}
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'un groupe - Graphiques Variation IPC par annee
@app.route('/api/var/<string:page>/', methods=['GET'])
def selectVar(page):
    conn = mysql.connect()
    cur = conn.cursor()

    label_groupe = group_map.get(page, None)
    if label_groupe is None:
        cur.close()
        conn.close()
        return make_response(jsonify({"error": "groupe inconnu"}), 400)

    cur.execute("""
    SELECT 
    fvg.annee,
    ROUND(fvg.variation_annuelle, 2) AS var_groupe
    FROM Fact_Variation_Groupe fvg
    JOIN Dim_Groupe g ON g.id_groupe = fvg.id_groupe
    WHERE g.label_grp = %s
    AND fvg.annee BETWEEN 2015 AND 2024
    ORDER BY fvg.annee;
    """, (label_groupe,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    labels = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]

    data = {"labels": labels, "data": values}
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'un groupe - Graphiques IPC Details sous-groupes
@app.route('/api/ipcDetails/<string:page>/<string:id_graph>', methods=['GET'])
def selectIpcDetails(page, id_graph):
    conn = mysql.connect()
    cur = conn.cursor()
    
    label_sous_grps = sous_groupe_map.get(id_graph, None) 
    
    if label_sous_grps is None:
        return make_response(jsonify({"error": "Invalid graph ID"}), 400)
    
    # Créer les placeholders SQL dynamiquement
    placeholders = ','.join(['%s'] * len(label_sous_grps))
    query = f"""
    SELECT 
        a.annee,
        sg.label_sous_grp,
        f.ipc
    FROM Fact_IPC f
    JOIN Dim_Sous_Groupe sg
        ON f.id_sous_groupe = sg.id_sous_groupe
    JOIN Dim_Annee a
        ON f.id_annee = a.id_annee
    WHERE sg.label_sous_grp IN ({placeholders})
      AND a.annee BETWEEN 2015 AND 2024
    ORDER BY a.annee;
    """
    
    cur.execute(query, tuple(label_sous_grps))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # Organiser les données par sous-groupe
    data_by_sous_groupe = {}
    all_years = set()
    
    for row in rows:
        annee = row[0]
        sous_grp = row[1]
        value = float(row[2])
        all_years.add(annee)
        
        if sous_grp not in data_by_sous_groupe:
            data_by_sous_groupe[sous_grp] = {}
        data_by_sous_groupe[sous_grp][annee] = value
    
    # Créer les datasets pour Chart.js
    all_years = sorted(list(all_years))
    datasets = []
    
    for sous_grp in label_sous_grps:
        if sous_grp in data_by_sous_groupe:
            values = [data_by_sous_groupe[sous_grp].get(year, 0) for year in all_years]
            datasets.append({
                "label": sous_grp,
                "data": values
            })
    
    data = {
        "labels": all_years,
        "datasets": datasets
    }
    return make_response(jsonify(data), 200)

# Definition des routes de la page d'un groupe - Graphiques Variation IPC Details sous-groupes
@app.route('/api/varDetails/<string:page>/<string:id_graph>', methods=['GET']) # slide 127 cours AJAX
def selectVarDetails(page, id_graph):
    conn = mysql.connect()
    cur = conn.cursor()
    
    label_sous_grps = sous_groupe_map.get(id_graph, None) 
    
    if label_sous_grps is None:
        return make_response(jsonify({"error": "Invalid graph ID"}), 400)
    
    # Créer les placeholders SQL dynamiquement
    placeholders = ','.join(['%s'] * len(label_sous_grps))
    query = f"""
    SELECT 
        a.annee,
        sg.label_sous_grp,
        f.variation
    FROM Fact_IPC f
    JOIN Dim_Sous_Groupe sg
        ON f.id_sous_groupe = sg.id_sous_groupe
    JOIN Dim_Annee a
        ON f.id_annee = a.id_annee
    WHERE sg.label_sous_grp IN ({placeholders})
      AND a.annee BETWEEN 2015 AND 2024
    ORDER BY a.annee;
    """
    
    cur.execute(query, tuple(label_sous_grps))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # Organiser les données par sous-groupe
    data_by_sous_groupe = {}
    all_years = set()
    
    for row in rows:
        annee = row[0]
        sous_grp = row[1]
        value = float(row[2])
        all_years.add(annee)
        
        if sous_grp not in data_by_sous_groupe:
            data_by_sous_groupe[sous_grp] = {}
        data_by_sous_groupe[sous_grp][annee] = value
    
    # Créer les datasets pour Chart.js
    all_years = sorted(list(all_years))
    datasets = []
    
    for sous_grp in label_sous_grps:
        if sous_grp in data_by_sous_groupe:
            values = [data_by_sous_groupe[sous_grp].get(year, 0) for year in all_years]
            datasets.append({
                "label": sous_grp,
                "data": values
            })
    
    data = {
        "labels": all_years,
        "datasets": datasets
    }
    print("\n \n Data for", page, id_graph,data)
    return make_response(jsonify(data), 200)

# *********************************** Definition des routes de la page d'export ***********************************

# Route pour l'export des donnees en CSV
@app.route("/api/export_csv", methods=["GET"])
def export_csv():
    dataset = request.args.get("dataset", "ipc_general")
    file_format = request.args.get("format", "csv").lower()

    conn = mysql.connect()
    cur = conn.cursor()

    if dataset == "ipc_general":
        filename_base = "ipc_general_2015_2024"
        header = ["annee", "ipc_general"]

        cur.execute("""
            SELECT annee, indice_general
            FROM evolution_globale
            ORDER BY annee;
        """)
        db_rows = cur.fetchall()
        rows = [(int(r[0]), float(r[1])) for r in db_rows]

    elif dataset == "var_general":
        filename_base = "variation_ipc_general_2015_2024"
        header = ["annee", "variation_ipc_general"]

        cur.execute("""
            SELECT annee, variation_pourcentage
            FROM evolution_globale
            ORDER BY annee;
        """)
        db_rows = cur.fetchall()
        rows = [(int(r[0]), float(r[1])) for r in db_rows]

    elif dataset == "all_dashboard":
        # ...existing code for all_dashboard...
        cur.execute("""
        SELECT
            a.annee,
            g.label_grp,
            sg.label_sous_grp,
            f.ipc,
            f.variation,
            g.poids_groupe,
            sg.poids_sous_groupe
        FROM Fact_IPC f
        JOIN Dim_Annee a        ON f.id_annee = a.id_annee
        JOIN Dim_Sous_Groupe sg ON f.id_sous_groupe = sg.id_sous_groupe
        JOIN Dim_Groupe g       ON f.id_groupe = g.id_groupe
        WHERE a.annee BETWEEN 2015 AND 2024
        ORDER BY a.annee, g.id_groupe, sg.id_sous_groupe;
        """)
        rows_raw = cur.fetchall()
        rows = []
        for (annee, groupe, sous_groupe, ipc, variation, poids_g, poids_sg) in rows_raw:
            rows.append((
                int(annee),
                str(groupe),
                str(sous_groupe),
                float(ipc),
                float(variation),
                float(poids_g),
                float(poids_sg),
            ))
    else:
        cur.close()
        conn.close()
        return make_response(jsonify({"error": "Dataset inconnu"}), 400)

    cur.close()
    conn.close()

    # --- Génération du fichier selon le format demandé ---

    if file_format == "xlsx":
        # Fichier Excel
        output = BytesIO()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "data"

        # Entête
        ws.append(header)
        # Lignes
        for row in rows:
            ws.append(list(row))

        wb.save(output)
        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename_base}.xlsx"}
        )

    else:
        # Fichier CSV (comportement d'origine)
        lines = [",".join(header) + "\n"]
        for row in rows:
            line = ",".join(str(v) for v in row)
            lines.append(line + "\n")
        csv_data = "".join(lines)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename_base}.csv"}
        )
    
# demarrer le serveur Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
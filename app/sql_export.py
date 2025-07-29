import sqlite3
import os
from datetime import datetime

def export_summary_from_sql(db_path="database/analizor.db", output_path="docs/synthese.txt", sql_file="sql/analyze.sql"):
    # Connexion à la base SQLite
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Lecture du fichier SQL complet
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Découper les requêtes sur les points-virgules
    requetes = [req.strip() + ";" for req in sql_content.strip().split(";") if req.strip()]

    # Exécution des requêtes dans l'ordre
    top_produits = cur.execute(requetes[0]).fetchall()
    ventes_par_ville = cur.execute(requetes[1]).fetchall()
    result = cur.execute(requetes[2]).fetchone()
    chiffre_affaires = result[0] if result and result[0] is not None else 0

    conn.close()

    # Création du dossier de sortie si besoin
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Écriture de la synthèse
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Fiche synthèse des résultats\n")
        f.write(f"Date de l'analyse : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("Top produits vendus :\n")
        for nom, quantite in top_produits:
            f.write(f"  - {nom} : {quantite} ventes\n")
        f.write("\n")

        f.write("Ventes par ville :\n")
        for ville, nb in ventes_par_ville:
            f.write(f"  - {ville} : {nb} ventes\n")
        f.write("\n")

        f.write(f"Chiffre d'affaires total : {chiffre_affaires:.2f} €\n")
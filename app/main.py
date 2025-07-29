from app.fetch import fetch_csv_data
from app.transform import transform_data
from app.db import get_connection, create_tables, insert_raw_data
from app.sql_export import export_summary_from_sql

# Étape 1 : Récupération des données brutes
def step1_fetch_data():
    """Télécharge les données et retourne les dataframes bruts."""
    return fetch_csv_data()

# Étape 2 : Transformation des données
def step2_transform_data(dataframes):
    """Transforme les dataframes et les retourne."""
    return transform_data(dataframes)

# Étape 3 : Chargement en base de données
def step3_load_to_db(transformed_data):
    """Crée la BDD et insère les données transformées."""
    produits, magasins, ventes = transformed_data
    conn = get_connection()
    create_tables(conn)
    insert_raw_data(conn, "produits", produits)
    insert_raw_data(conn, "magasins", magasins)
    insert_raw_data(conn, "ventes", ventes)
    conn.close()
    return "Base de données créée et chargée avec succès."

# Étape 4 : Génération de la synthèse
def step4_generate_summary():
    """Exécute les requêtes SQL et retourne le rapport final."""
    summary_path = "docs/synthese.txt"
    export_summary_from_sql(output_path=summary_path)
    with open(summary_path, 'r', encoding='utf-8') as f:
        return f.read()
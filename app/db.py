import os
import sqlite3
import logging

def get_connection():
    # Création du dossier 'database' si nécessaire
    db_path = "database/analizor.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connexion à la base SQLite
    return sqlite3.connect(db_path)

def create_tables(conn):
    cur = conn.cursor()

    # Création de la table produits
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id_produit TEXT PRIMARY KEY,
            nom TEXT,
            prix REAL,
            stock INTEGER
        );
    """)
    logging.info('Création de la table "produits"')

    # Création de la table magasins
    cur.execute("""
        CREATE TABLE IF NOT EXISTS magasins (
            id_magasin TEXT PRIMARY KEY,
            ville TEXT,
            nb_salaries INTEGER
        );
    """)
    logging.info('Création de la table "magasins"')

    # Création de la table ventes avec une contrainte UNIQUE pour éviter les doublons
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            id_magasin TEXT,
            id_produit TEXT,
            quantite INTEGER,
            UNIQUE(date, id_magasin, id_produit, quantite)
        );
    """)
    logging.info('Création de la table "ventes"')

    # Enregistrement des changements dans la base
    conn.commit()

def insert_raw_data(conn, table, df):
    cur = conn.cursor()

    if table == "produits":
        cur.executemany("""
            INSERT OR IGNORE INTO produits (id_produit, nom, prix, stock)
            VALUES (?, ?, ?, ?)
        """, df.values.tolist())

    elif table == "magasins":
        cur.executemany("""
            INSERT OR IGNORE INTO magasins (id_magasin, ville, nb_salaries)
            VALUES (?, ?, ?)
        """, df.values.tolist())

    elif table == "ventes":
        cur.executemany("""
            INSERT OR IGNORE INTO ventes (date, id_magasin, id_produit, quantite)
            VALUES (?, ?, ?, ?)
        """, df[["date", "id_magasin", "id_produit", "quantite"]].values.tolist())

    conn.commit()
    logging.info(f'Données insérées dans la table "{table}"')
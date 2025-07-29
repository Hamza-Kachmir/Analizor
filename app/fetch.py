import os
import pandas as pd
import logging
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

def fetch_csv_data():
    # Dictionnaire des URLs des fichiers CSV à télécharger, récupérées depuis les variables d'environnement
    urls = {
        "produits": os.getenv("CSV_URL_PRODUITS"),
        "magasins": os.getenv("CSV_URL_MAGASINS"),
        "ventes": os.getenv("CSV_URL_VENTES")
    }

    dataframes = {}

    # Pour chaque type de donnée, on lit le CSV et on l'ajoute dans un dictionnaire
    for key, url in urls.items():
        df = pd.read_csv(url)
        logging.info(f'Fichier "{key}" téléchargé avec succès')
        dataframes[key] = df

    # Retourne un dictionnaire contenant les DataFrames
    return dataframes
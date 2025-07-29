def transform_data(dataframes):
    # Récupération des DataFrames bruts téléchargés depuis les CSV
    produits = dataframes["produits"]
    magasins = dataframes["magasins"]
    ventes = dataframes["ventes"]

    # === Nettoyage et harmonisation des colonnes ===

    # Les colonnes du CSV produits sont dans l'ordre : nom, id_produit, prix, stock
    # On commence par les renommer clairement
    produits.columns = ["nom", "id_produit", "prix", "stock"]
    
    # On réorganise les colonnes pour correspondre au schéma de la base : id_produit | nom | prix | stock
    produits = produits[["id_produit", "nom", "prix", "stock"]]

    # Renommage des colonnes pour les magasins
    magasins.columns = ["id_magasin", "ville", "nb_salaries"]

    # Renommage des colonnes pour les ventes
    ventes.columns = ["date", "id_produit", "quantite", "id_magasin"]

    # Réorganisation des colonnes des ventes pour les insérer correctement
    ventes = ventes[["date", "id_magasin", "id_produit", "quantite"]]

    # On retourne les trois DataFrames prêts à être insérés en base
    return produits, magasins, ventes
-- Requête top produits vendus
SELECT p.nom, SUM(v.quantite) AS total_vendu
FROM ventes v
JOIN produits p ON v.id_produit = p.id_produit
GROUP BY p.nom
ORDER BY total_vendu DESC
LIMIT 3;

-- Requête ventes par ville
SELECT m.ville, COUNT(*) AS nombre_de_ventes
FROM ventes v
JOIN magasins m ON v.id_magasin = m.id_magasin
GROUP BY m.ville
ORDER BY nombre_de_ventes DESC;

-- Requête Chiffre d'affaires total
SELECT SUM(p.prix * v.quantite) AS chiffre_affaires
FROM ventes v
JOIN produits p ON v.id_produit = p.id_produit;
# Analizor

Une application web de démonstration pour un pipeline de données (ETL) interactif, développée avec Python, Pandas, SQL et Docker.

---

### 🚀 Contexte du Projet

Ce projet a été réalisé dans le cadre de mon admission à une formation de **Data Engineer**. L'objectif était de démontrer la maîtrise des étapes fondamentales d'un pipeline de données.

**Analizor** est donc une démonstration technique de ce processus de bout en bout : récupérer des données brutes de sources externes, les nettoyer et les structurer, les charger dans une base de données, puis les analyser pour en extraire des informations pertinentes.

### 🛠️ À propos de cette démo interactive

Cette application web a été créée pour rendre ce processus technique visible et interactif. Plutôt que de simplement exécuter un script en arrière-plan, l'interface vous guide à travers chaque étape du pipeline, vous permettant de voir les données évoluer en temps réel.

Le pipeline se déroule en 4 étapes contrôlées par l'utilisateur :

1.  **Étape 1 : Extract (Extraction)**
    Les données brutes sur les produits, magasins et ventes sont téléchargées depuis des fichiers CSV distants.

2.  **Étape 2 : Transform (Transformation)**
    Les données sont nettoyées, les colonnes sont renommées et réorganisées à l'aide de la librairie **Pandas** pour être prêtes à être insérées en base de données.

3.  **Étape 3 : Load (Chargement)**
    Les données transformées sont chargées dans une base de données **SQLite**. Les tables sont créées et peuplées.

4.  **Étape 4 : Analysis & Reporting**
    Des requêtes **SQL** sont exécutées sur la base de données pour calculer des indicateurs clés (top des ventes, chiffre d'affaires...). Une fiche de synthèse est alors générée et affichée.

---

### ⚙️ Technologies Utilisées

* **Langage :** Python
* **Analyse de Données :** Pandas
* **Base de Données :** SQLite
* **Framework Web / UI :** NiceGUI
* **Conteneurisation :** Docker
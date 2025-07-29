import os
from nicegui import ui, app, run
import pandas as pd
from app.main import (
    step1_fetch_data,
    step2_transform_data,
    step3_load_to_db,
    step4_generate_summary,
)

@ui.page('/')
def main_page():
    # Initialisation de l'état de la démo pour chaque utilisateur
    app.storage.user['step'] = 0
    app.storage.user['data'] = None

    with ui.row().classes('w-full justify-center'):
        ui.label('Démo Analizor').classes('text-3xl font-bold my-4')

    # Zone unique pour les messages d'état et les résultats
    output_area = ui.column().classes('w-full items-center gap-4')

    # Conteneur pour les boutons
    with ui.row().classes('w-full justify-center mt-8 gap-4'):
        next_button = ui.button("Démarrer le Pipeline (Étape 1/4)", on_click=lambda: run_next_step())
        reset_button = ui.button("Recommencer", on_click=lambda: reset_demo())
    
    def reset_demo():
        """Réinitialise la démo à son état initial."""
        app.storage.user['step'] = 0
        app.storage.user['data'] = None
        next_button.text = "Démarrer le Pipeline (Étape 1/4)"
        next_button.enable()
        output_area.clear()

    async def run_next_step():
        """Fonction 'contrôleur' qui exécute la bonne étape en fonction de l'état."""
        step = app.storage.user.get('step', 0)
        
        # On nettoie la zone de sortie à chaque nouvelle étape
        output_area.clear()
        with output_area:
            ui.spinner(size='lg')
            ui.label("Étape en cours...").classes('self-center ml-4')
        
        next_button.disable()

        try:
            if step == 0:
                # Étape 1: Fetch
                dataframes = await run.io_bound(step1_fetch_data)
                serializable_data = {name: df.to_dict('records') for name, df in dataframes.items()}
                app.storage.user['data'] = serializable_data
                
                output_area.clear()
                with output_area:
                    ui.label("Étape 1: Données brutes téléchargées").classes('text-xl font-bold')
                    for name, df_dict in serializable_data.items():
                        ui.label(f"Aperçu du fichier '{name}.csv' :").classes('text-lg')
                        if df_dict:
                            ui.table(columns=[{'name': col, 'label': col, 'field': col} for col in df_dict[0].keys()],
                                     rows=df_dict[:5]).classes('w-full max-w-4xl')
                        else:
                            ui.label("Fichier vide ou non trouvé.")
                
                app.storage.user['step'] = 1
                next_button.text = "Lancer la Transformation (Étape 2/4)"

            elif step == 1:
                # Étape 2: Transform
                serializable_data = app.storage.user['data']
                dataframes = {name: pd.DataFrame.from_records(data) for name, data in serializable_data.items()}
                
                transformed_data = await run.io_bound(step2_transform_data, dataframes)
                p, m, v = transformed_data
                app.storage.user['data'] = [p.to_dict('records'), m.to_dict('records'), v.to_dict('records')]

                output_area.clear()
                with output_area:
                    ui.label("Étape 2: Données transformées et nettoyées").classes('text-xl font-bold')
                    ui.label("Aperçu des données de ventes prêtes pour l'insertion :").classes('text-lg')
                    ui.table(columns=[{'name': col, 'label': col, 'field': col} for col in v.columns],
                             rows=v.head().to_dict('records')).classes('w-full max-w-4xl')

                app.storage.user['step'] = 2
                next_button.text = "Charger en Base de Données (Étape 3/4)"

            elif step == 2:
                # Étape 3: Load
                p_dict, m_dict, v_dict = app.storage.user['data']
                transformed_data_dfs = (pd.DataFrame.from_records(p_dict), pd.DataFrame.from_records(m_dict), pd.DataFrame.from_records(v_dict))

                message = await run.io_bound(step3_load_to_db, transformed_data_dfs)
                
                output_area.clear()
                with output_area:
                    ui.label("Étape 3: Chargement en Base de Données").classes('text-xl font-bold')
                    ui.chip(message, icon='task_alt').classes('bg-green-600 text-white p-4 text-lg')

                app.storage.user['step'] = 3
                next_button.text = "Générer la Synthèse (Étape 4/4)"

            elif step == 3:
                # Étape 4: Summary
                summary = await run.io_bound(step4_generate_summary)

                output_area.clear()
                with output_area:
                    ui.label("Étape 4: Synthèse finale").classes('text-xl font-bold')
                    ui.markdown(f"```\n{summary}\n```").classes('w-full max-w-2xl bg-gray-100 p-4 rounded')
                
                app.storage.user['step'] = 4
                next_button.text = "Pipeline Terminé !"
            
            if app.storage.user['step'] < 4:
                next_button.enable()

        except Exception as e:
            output_area.clear()
            ui.notification(f"Une erreur est survenue : {e}", color='negative')
            next_button.text = "Erreur - Recommencer"
            next_button.enable()

# Lancement de l'application web
port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port, title="Analizor", storage_secret='UNE_CLE_SECRETE_POUR_LA_SESSION')
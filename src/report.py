import os
import pandas as pd

def generate_excel_report(df_communes: pd.DataFrame, mix_data: tuple, output_path: str = "data/rapport_velib.xlsx"):
    """Génère un fichier Excel avec deux onglets pour le rapport."""
    
    # S'assurer que le dossier de sortie existe (data/)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # On prépare les données du Mix de vélos pour en faire un petit tableau propre
    nb_elec, nb_meca, part_elec, part_meca = mix_data
    df_mix = pd.DataFrame({
        "Indicateur": ["Nombre total", "Proportion (%)"],
        "Vélos Électriques": [nb_elec, f"{part_elec:.2f}%"],
        "Vélos Mécaniques": [nb_meca, f"{part_meca:.2f}%"]
    })
    
    # On utilise ExcelWriter pour écrire plusieurs onglets dans le même fichier
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # dans la feuille 1 : j'analyse les données par commune
        df_communes.to_excel(writer, sheet_name="Analyse Communes", index=True)
        
        # la feuille 2 
        df_mix.to_excel(writer, sheet_name="Mix Électrique Mécanique", index=False)
        
    print(f"Le rapport Excel a été généré avec succès ici : {output_path}")
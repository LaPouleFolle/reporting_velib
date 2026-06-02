import os
import requests
from io import BytesIO
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from src.report import generate_excel_report

def main():

    # importation des données
    url = "https://minio.lab.sspcloud.fr/demon/velib/data/brute/velib-disponibilite-en-temps-reel.parquet"
    print("le fichier parquet est op")
    
    response = requests.get(url)
    response.raise_for_status()

    with BytesIO(response.content) as buffer:
        gdf = gpd.read_parquet(buffer)
    
    # On crée une figure simple avec matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # affichage des station grace aux point
    gdf.plot(column='numbikesavailable', cmap='coolwarm', legend=True, 
             markersize=15, ax=ax, legend_kwds={'label': "Nombre de vélos disponibles"})
    
    ax.set_title("Disponibilité des Vélib' en Temps Réel", fontsize=14)
    ax.set_axis_off() # ici c'est pour enléver les axe de coordonnée pour un rendu plus lisible quoi
    
    # On s'assure que le dossier 'data' existe et on sauvegarde l'image
    os.makedirs("data", exist_ok=True)
    chemin = "data/carte_velib.png"
    plt.savefig(chemin, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"image de la carte sauvegardée ici : {chemin}")
    

    df_excel = pd.DataFrame(gdf)
    
    # on convertit en texte la colonne géo
    if 'geometry' in df_excel.columns:
        df_excel['geometry'] = df_excel['geometry'].astype(str)

    # Nettoyage des fuseaux horaires pour Excel
    for col in df_excel.columns:
        if pd.api.types.is_datetime64_any_dtype(df_excel[col]):
            if df_excel[col].dt.tz is not None:
                df_excel[col] = df_excel[col].dt.tz_localize(None)
                
    # j'envoi les données au rapport Excel
    generate_excel_report(df_excel, output_path="data/rapport_velib.xlsx")
    
    print("fin du programme")

if __name__ == "__main__":
    main()
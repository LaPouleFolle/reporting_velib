import os
import requests
from io import BytesIO
import geopandas as gpd
import pandas as pd
import folium
# CHANGEMENT ICI : Importations adaptées à la nouvelle structure "src layout"
from reporting_velib.report import generate_excel_report
from reporting_velib.utils import clean_data, compute_commune_analysis
from reporting_velib.config import URL_DATA_VELIB, OUTPUT_EXCEL, OUTPUT_CARTE

def main():
    # importation des données 
    print("téléchargement des données Vélib")
    response = requests.get(URL_DATA_VELIB)
    response.raise_for_status()

    with BytesIO(response.content) as buffer:
        gdf = gpd.read_parquet(buffer)
    
    # j'appel de les fonctions de calcul  du top des communes
    print("nettoyage et calcul du Top 5 des communes...")
    df_clean = pd.DataFrame(gdf)
    df_clean = clean_data(df_clean) # Calcule l'occupation_rate
    df_top5 = compute_commune_analysis(df_clean).head(5).reset_index() # Calcule ton Top 5
    
    # Création et sauvegarde de la carte spatiale
    # on crée une carte centrée sur Paris (Latitude: 48.8566, Longitude: 2.3522)
    carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
    
    # our ne pas faire ramer l'ordinateur, on affiche les 100 premières stations
    df_carte = gdf.head(100)
    
    for idx, row in df_carte.iterrows():
        lat = row['coordonnees_geo'].y
        lon = row['coordonnees_geo'].x
        nom_station = row['name']
        velos_dispos = row['numbikesavailable']
        
        # on ajoute un petit marqueur sur la carte pour chaque station
        folium.Marker(
            location=[lat, lon],
            popup= f"Station : {nom_station}<br>Vélos disponibles : {velos_dispos}",
            icon = folium.Icon(color="blue", icon="info-sign")
        ).add_to(carte)
    
    #  s'assure que le dossier 'data' existe et on sauvegarde au format WEB (HTML)
    os.makedirs("data", exist_ok=True)
    carte.save(OUTPUT_CARTE)
    print(f"ma carte se trouve ici : {OUTPUT_CARTE}")
    
    # on copie les donnée déjà nettoyé
    df_excel = df_clean.copy() 
    
    if 'geometry' in df_excel.columns:
        df_excel['geometry'] = df_excel['geometry'].astype(str)

    # Nettoyage des fuseaux horaires pour Excel
    for col in df_excel.columns:
        if pd.api.types.is_datetime64_any_dtype(df_excel[col]):
            if df_excel[col].dt.tz is not None:
                df_excel[col] = df_excel[col].dt.tz_localize(None)
                
    # créat° du dashboard
    print("création du Tableau de Bord Excel")
    
    generate_excel_report(df_excel, df_top5, output_path=OUTPUT_EXCEL)
    print("le programme est op")

if __name__ == "__main__":
    main()
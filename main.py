import os
import pandas as pd
import s3fs
from src.report import generate_excel_report

def main():
    print("Démarrage du pipeline Vélib' (Création complète de zéro)...")

    # 1. Connexion sécurisée à Onyxia
    fs = s3fs.S3FileSystem(
        key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        token=os.environ.get("AWS_SESSION_TOKEN"),
        client_kwargs={'endpoint_url': 'https://minio.lab.sspcloud.fr'}
    )
    
    URL_S3 = "demon/velib/data/brute/velib-disponibilite-en-temps-reel.parquet"
    
    # 2. Chargement des données brutes
    print("Récupération des données en direct...")
    with fs.open(URL_S3, mode='rb') as f:
        df = pd.read_parquet(f)
    
    # --- NETTOYAGE DES DATES POUR EXCEL ---
    # On détecte les colonnes de type date et on retire le fuseau horaire
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_localize(None)
                
    # 3. Génération autonome du rapport Excel
    print("Création des onglets, des formules et du graphique...")
    generate_excel_report(df, output_path="data/rapport_velib.xlsx")
    
    print("Fin du programme. Le fichier Excel est complet et le graphique est vivant !")

if __name__ == "__main__":
    main()
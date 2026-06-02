import os
import pandas as pd
import s3fs
from src.report import generate_excel_report

def main():
    print("Démarrage du pipeline Vélib' (Création complète de zéro)...")

    # connexion à Onyxia
    fs = s3fs.S3FileSystem(
        key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        token=os.environ.get("AWS_SESSION_TOKEN"),
        client_kwargs={'endpoint_url': 'https://minio.lab.sspcloud.fr'}
    )
    
    URL_S3 = "demon/velib/data/brute/velib-disponibilite-en-temps-reel.parquet"
    
    # chargement des données 
    print("récupération des données ...")
    with fs.open(URL_S3, mode='rb') as f:
        df = pd.read_parquet(f)
    
    # --- le nettoyage des dates; comment je vais gérer ça sur excel? appliqué un format? bah c'est possible en fait ---
    # ppour les colonnes de type date et je retire le fuseau horaire
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_localize(None)
                
    # génération autonome du rapport Excel
    generate_excel_report(df, output_path="data/rapport_velib.xlsx")
    
    print("fin du programme, seigneur merci vrai vrai")

if __name__ == "__main__":
    main()
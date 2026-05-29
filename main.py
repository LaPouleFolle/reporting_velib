import os
import pandas as pd
import s3fs
from src.utils import clean_data, compute_bike_mix, compute_commune_analysis
from src.report import generate_excel_report

def main():
    # Connexion à Onyxia (je devrai modifier cette façon de se connecter comme la suggérer le prof)
    fs = s3fs.S3FileSystem(
        key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        token=os.environ.get("AWS_SESSION_TOKEN"),
        client_kwargs={'endpoint_url': 'https://minio.lab.sspcloud.fr'}
    )
    
    # Chemin du fichier Parquet
    URL_S3 = "demon/velib/data/brute/velib-disponibilite-en-temps-reel.parquet"
    
    # chargement des données à jour
    with fs.open(URL_S3, mode='rb') as f:
        df = pd.read_parquet(f)
    print(f"mes data ({len(df)}")

    # Nettoyage des donnée et calculs
    df = clean_data(df)
    mix_results = compute_bike_mix(df)
    df_communes = compute_commune_analysis(df)

    # on va généré le rapport Excel
    ## mettre un titre avec un print("création du rapport?")
    generate_excel_report(df_communes, mix_results, output_path="data/rapport_velib.xlsx")
    
    print("Fin du programme")

if __name__ == "__main__":
    main()
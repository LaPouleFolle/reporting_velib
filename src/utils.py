import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le taux d'occupation des stations."""
    # je calcul le taux d'occupation des stations velib 
    df['occupation_rate'] = df['numbikesavailable'] / df['capacity']
    df['occupation_rate'] = df['occupation_rate'] * 100
    
    # valeurs infinies par 0 pour facilité les calculs
    df['occupation_rate'] = df['occupation_rate'].replace(np.inf, 0)
    return df

def compute_bike_mix(df: pd.DataFrame):
    """Calcule la proportion de vélos électriques et mécaniques"""
    nb_total_electrique = df['ebike'].sum()
    nb_total_mecanique = df['mechanical'].sum()
    n = df['numbikesavailable'].sum()
    
    part_electrique = (nb_total_electrique / n) * 100
    part_mecanique = (nb_total_mecanique / n) * 100
    
    return nb_total_electrique, nb_total_mecanique, part_electrique, part_mecanique

def compute_commune_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """calcule les moyennes de disponibilité et d'occupation par commune."""
    commune = df.groupby('nom_arrondissement_communes')[['numbikesavailable', 'occupation_rate']].mean()
    commune = commune.sort_values(by='numbikesavailable', ascending=False)
    return commune
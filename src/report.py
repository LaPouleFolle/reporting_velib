import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from openpyxl.utils import get_column_letter
#from openpyxl.drawing.image import Image # ajout de l'image pour ma carte figé
from openpyxl.worksheet.datavalidation import DataValidation

# =========================================================================
# FONCTIONS SPÉCIALISÉES (Chacune gère une seule action de la liste)
# =========================================================================

def _creation_du_dossier(output_path):
    # on créé le dossier
    os.makedirs(os.path.dirname(output_path), exist_ok=True)


def _onglet_data(df_raw, output_path):
    # mon onglet data dans le fichier excel
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_raw.to_excel(writer, sheet_name="DATA", index=False)


def _ouverture_du_fichier(output_path):
    # ouvertur du fichier
    return load_workbook(output_path)


def _indicateurs(wb):
    # l'onglet indicator ou je vais mettre mes graph
    ws = wb.create_sheet("Indicateurs")

    # le titre du rapport
    ws["A3"] = "TABLEAU DE BORD DU RÉSEAU VÉLIB"
    ws["A3"].font = Font(bold=True, size=14)
    return ws


def _liste_deroulante_communes(ws, df_raw):
    # on ajoute le label et la liste en B1
    ws["A1"] = "Choisir une commune :"
    ws["A1"].font = Font(bold=True, color="0000FF") # Mis en bleu pour attirer l'œil
    ws["B1"] = "Paris" # Valeur par défaut obligatoire

    # TECHNIQUE SÉCURISÉE : Extraction des communes uniques pour éviter les doublons et les bugs de longueur Excel
    communes_uniques = sorted(df_raw['nom_arrondissement_communes'].dropna().unique())
    
    # Construction de la chaîne de caractères entourée de guillemets pour Excel
    liste_communes_txt = f'"{",".join(communes_uniques)}"'
    
    # On crée la validation en lui donnant la chaîne de texte formatée
    dv = DataValidation(type="list", formula1=liste_communes_txt, allow_blank=True)
    
    dv.error = "Votre commune n'est pas dans la liste"
    dv.errorTitle = "Saisie invalide"
    dv.prompt = "SVP choisissez une commune dans la liste"
    dv.promptTitle = "Liste des communes"

    # IMPORTANT : On ajoute la validation à la feuille PUIS on l'associe à la cellule
    ws.add_data_validation(dv)
    dv.add(ws["B1"])


def _recup_colonne(df_raw):
    # je recupere les colonnes 
    headers = list(df_raw.columns)

    col_capacity = headers.index("capacity") + 1
    col_docks = headers.index("numdocksavailable") + 1
    col_bikes = headers.index("numbikesavailable") + 1
    col_meca = headers.index("mechanical") + 1
    col_ebike = headers.index("ebike") + 1

    # 
    return {
        "capacity": get_column_letter(col_capacity),
        "docks": get_column_letter(col_docks),
        "bikes": get_column_letter(col_bikes),
        "meca": get_column_letter(col_meca),
        "ebike": get_column_letter(col_ebike)
    }


def _kpi_du_reseau(ws, cols, max_row):
    #  indicateurs réseau velib
    ws["A4"] = "Indicateurs Réseau"
    ws["A4"].font = Font(bold=True, underline="single")

    # Utilisation de SUMIF pour filtrer dynamiquement en fonction de la valeur rentrer dans ma cellule B1
    ws["A5"] = "Capacité totale"
    ws["B5"] = f'=SUMIF(DATA!M2:M{max_row}, B1, DATA!{cols["capacity"]}2:{cols["capacity"]}{max_row})'

    ws["A6"] = "Bornettes libres"
    ws["B6"] = f'=SUMIF(DATA!M2:M{max_row}, B1, DATA!{cols["docks"]}2:{cols["docks"]}{max_row})'

    ws["A7"] = "Total vélos disponibles"
    ws["B7"] = f'=SUMIF(DATA!M2:M{max_row}, B1, DATA!{cols["bikes"]}2:{cols["bikes"]}{max_row})'

    ws["A8"] = "Taux d'occupation global"
    ws["B8"] = "=B7/B5"
    ws["B8"].number_format = "0.00%"


def _kpi_du_types_velos(ws, cols, max_row):
    # mes indicateurs sur les types de vélos
    ws["A11"] = "Répartition par type de vélo"
    ws["A11"].font = Font(bold=True, underline="single")

    ws["A12"] = "Vélos mécaniques"
    ws["B12"] = f'=SUMIF(DATA!M2:M{max_row}, B1, DATA!{cols["meca"]}2:{cols["meca"]}{max_row})'

    ws["A13"] = "Vélos électriques"
    ws["B13"] = f'=SUMIF(DATA!M2:M{max_row}, B1, DATA!{cols["ebike"]}2:{cols["ebike"]}{max_row})'

    ws["A14"] = "Total vélos vérifié"
    ws["B14"] = "=SUM(B12:B13)"


def _top5_communes(ws, df_top5):
    # top 5 des communes 
    ws["A17"] = "Top 5 des communes les plus desservies en vélo"
    ws["A17"].font = Font(bold=True, underline="single")

    # On utilise les données calculées par compute_commune_analysis
    for idx, row in df_top5.iterrows():
        ligne_actuelle = 18 + idx
        ws["A" + str(ligne_actuelle)] = row['nom_arrondissement_communes']
        ws["B" + str(ligne_actuelle)] = round(row['numbikesavailable'], 1)
        ws["C" + str(ligne_actuelle)] = round(row['occupation_rate'] * 100, 1)


def _graphiques(ws):
    # Graphique en secteur
    pie = PieChart()
    pie.title = "Types de vélos disponibles"

    data_pie = Reference(ws, min_col=2, min_row=12, max_row=13)
    labels_pie = Reference(ws, min_col=1, min_row=12, max_row=13)

    pie.add_data(data_pie)
    pie.set_categories(labels_pie)

    ws.add_chart(pie, "E4")

    # barplot
    bar = BarChart()
    bar.title = "Disponibilité globale du réseau"
    bar.y_axis.title = "Quantité"
    bar.width = 15  
    bar.height = 10

    data_bar = Reference(ws, min_col=2, min_row=5, max_row=7)
    labels_bar = Reference(ws, min_col=1, min_row=5, max_row=7)

    bar.add_data(data_bar)
    bar.set_categories(labels_bar)
    bar.legend = None

    ws.add_chart(bar, "N4")

    # Graphique en barre combiné 
    # l'histogramme du nbre de vélos
    chart_velo = BarChart()
    chart_velo.title = "Nombre de vélo par occupation dans chaque commune du top"
    chart_velo.style = 10 ### cette commande c'est pour gérer le stype du graphique style de base 10
    chart_velo.width = 15   # Largeur en cm 
    chart_velo.height = 12  ### la hauteur du graph
    chart_velo.y_axis.title = "Nombre moyen de vélos"
    chart_velo.x_axis.title = "Communes"

    data_velo = Reference(ws, min_col=2, min_row=18, max_row=22)
    labels_communes = Reference(ws, min_col=1, min_row=18, max_row=22)
    chart_velo.add_data(data_velo)
    chart_velo.set_categories(labels_communes)
    chart_velo.legend = None

    # création de la ligne du taux d'occupat°
    chart_line = LineChart()
    data_occupation = Reference(ws, min_col=3, min_row=18, max_row=22)
    chart_line.add_data(data_occupation)
    
    # Concatenat) des 2 graphiques 
    chart_line.y_axis.axId = 200
    chart_line.y_axis.title = "Taux d'occupation en (%)"
    chart_line.y_axis.crosses = "max"
    chart_velo += chart_line

    ws.add_chart(chart_velo, "E18")


def _sauvegarde(wb, output_path):
    # je sauvegarde quand même
    wb.save(output_path)
    wb.close()

    print("le fichier excel est op :", output_path)


# La fonction principale
def generate_excel_report(df_raw, df_top5, output_path="data/rapport_velib.xlsx"):
    
    _creation_du_dossier(output_path)
    _onglet_data(df_raw, output_path)
    
    wb = _ouverture_du_fichier(output_path)
    
    # Nombre de lignes dans mon jeu de donnée, ici je compte avec len() c'est la bonne methode? 
    max_row = len(df_raw) + 1

    ws = _indicateurs(wb)
    
    # "ajout de la liste déroulante pour le filtre "
    _liste_deroulante_communes(ws, df_raw)
    
    cols = _recup_colonne(df_raw)
    
    _kpi_du_reseau(ws, cols, max_row)
    _kpi_du_types_velos(ws, cols, max_row)
    _top5_communes(ws, df_top5)
    _graphiques(ws)
    
    _sauvegarde(wb, output_path)
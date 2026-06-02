import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.chart import BarChart, PieChart, Reference


def generate_excel_report(df_raw, output_path="data/rapport_velib.xlsx"):

    # on créé le dossier
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # mon onglet data dans le fichier excel
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_raw.to_excel(writer, sheet_name="DATA", index=False)

    # ouvertur du fichier
    wb = load_workbook(output_path)

    # l'onglet indicateur ou je vais mettre mes graph
    ws = wb.create_sheet("Indicateurs")

    # Nombre de lignes dans mon jeu de donnée, ici je compte avec len() c'est la bonne methode? 
    max_row = len(df_raw) + 1

    # je recupere les colonnes 
    headers = list(df_raw.columns)

    col_capacity = headers.index("capacity") + 1
    col_docks = headers.index("numdocksavailable") + 1
    col_bikes = headers.index("numbikesavailable") + 1
    col_meca = headers.index("mechanical") + 1
    col_ebike = headers.index("ebike") + 1

    # 
    from openpyxl.utils import get_column_letter

    col_capacity = get_column_letter(col_capacity)
    col_docks = get_column_letter(col_docks)
    col_bikes = get_column_letter(col_bikes)
    col_meca = get_column_letter(col_meca)
    col_ebike = get_column_letter(col_ebike)

    # le titre du rapport
    ws["A3"] = "TABLEAU DE BORD DU RÉSEAU VÉLIB"
    ws["A3"].font = Font(bold=True, size=14)

    #  indicateurs réseau velib
    ws["A4"] = "Indicateurs Réseau"
    ws["A4"].font = Font(bold=True, underline="single")

    ws["A5"] = "Capacité totale"
    ws["B5"] = f"=SUM(DATA!{col_capacity}2:{col_capacity}{max_row})"

    ws["A6"] = "Bornettes libres"
    ws["B6"] = f"=SUM(DATA!{col_docks}2:{col_docks}{max_row})"

    ws["A7"] = "Total vélos disponibles"
    ws["B7"] = f"=SUM(DATA!{col_bikes}2:{col_bikes}{max_row})"

    ws["A8"] = "Taux d'occupation global"
    ws["B8"] = "=B7/B5"
    ws["B8"].number_format = "0.00%"

    # mes indicateurs sur les types de vélos
    ws["A11"] = "Répartition par type de vélo"
    ws["A11"].font = Font(bold=True, underline="single")

    ws["A12"] = "Vélos mécaniques"
    ws["B12"] = f"=SUM(DATA!{col_meca}2:{col_meca}{max_row})"

    ws["A13"] = "Vélos électriques"
    ws["B13"] = f"=SUM(DATA!{col_ebike}2:{col_ebike}{max_row})"

    ws["A14"] = "Total vélos vérifié"
    ws["B14"] = "=SUM(B12:B13)"

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

    data_bar = Reference(ws, min_col=2, min_row=5, max_row=7)
    labels_bar = Reference(ws, min_col=1, min_row=5, max_row=7)

    bar.add_data(data_bar)
    bar.set_categories(labels_bar)
    bar.legend = None

    ws.add_chart(bar, "E18")

    # je sauvegarde quand même
    wb.save(output_path)
    wb.close()

    print("le fichier excel est op :", output_path)
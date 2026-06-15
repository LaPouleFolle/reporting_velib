# Reporting Automatisé - Réseau Vélib Métropole

## Objectifs du projet
Ce projet a pour but de concevoir un système de reporting combinant Python et Excel. L'objectif est d'analyser la proportion de vélos électriques par rapport aux vélos mécaniques , tout en comparant la disponibilité et l’occupation des stations par commune afin de fournir un tableau de bord d'aide à la décision.

## Source des données et Dictionnaire de donnée

### Source des donnée
Les données proviennent de la plateforme Paris Data et représentent la disponibilité du réseau Vélib' Métropole (1511 stations réparties sur Paris et la petite couronne).
- **Lien :** [Paris Open Data - Disponibilité Vélib](https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/)

### Dictionnaire des données clés
- `stationcode` : Identifiant unique (clé primaire) de la station.
- `name` : Nom de la station (libellé de l'emplacement).
- `is_installed` : État de fonctionnement de la station (OUI/NON).
- `capacity` : Capacité totale de la station (nombre de bornes max).
- `numdocksavailable` : Nombre de bornettes libres (places disponibles pour déposer un vélo).
- `numbikesavailable` : Nombre total de vélos disponibles (Somme des mécaniques et électriques).
- `mechanical` : Nombre de vélos mécaniques (classiques) disponibles.
- `ebike` : Nombre de vélos électriques disponibles.
- `nom_arrondissement_communes` : Nom de la commune ou de l'arrondissement parisien.
- `code_insee_commune` : Code administratif INSEE de la commune.
- `coordonnees_geo` : Coordonnées géographiques (Latitude et Longitude de la station).
- `occupation_rate` : Taux d'occupation de la station calculé (`numbikesavailable / capacity`).

## Le Schéma du projet et Architecture
Le projet respecte l'architecture standard **src layout** vue en cour notamment :

reporting_velib/
├── data/                       # il contient le rapport générés et la carte au format png des stations de velib
├── notebooks/
│   └── exploration.ipynb       # analyse exploratoire et graphiques 
├── src/
│   └── reporting_velib/        # code et package
│       ├── init.py
│       ├── config.py           # configuration (URLs, chemins de donnée)
│       ├── report.py           # pour généré le Dashboard excel avec openxl
│       ├── utils.py            # fonctions de nettoyage et calculs 
│       └── main.py             # Script principal 
├── pyproject.toml              # Configuration du projet 
└── uv.lock

Ce projet utilise Uv pour une gestion rapide des dépendances, et pour lancé le projet, il faut exécuter la commande uv run velib

## Maquette du rapport

Cette maquette est une prévisualisation de mon rapport qui n'est pas définitive : 

Maquette finale: 
<img width="750" height="385" alt="image" src="https://github.com/user-attachments/assets/4a7e956d-6abf-4ceb-b066-3a7516080ec9" />



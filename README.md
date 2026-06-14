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
├── data/
├── notebooks/
├── src/
│   └── reporting_velib/
│       ├── __init__.py
│       ├── config.py
│       ├── report.py
│       ├── utils.py
│       └── main.py
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock

Ce projet utilise Uv pour une gestion rapide des dépendances, et pour lancé le projet, il faut exécuter la commande uv run velib

## Maquette du rapport

Cette maquette est une prévisualisation de mon rapport qui n'est pas définitive : 

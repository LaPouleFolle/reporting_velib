# reporting_velib
Projet outil de donnée

Vélib’ Métropole est le premier service mondial de vélos en libre-service, couvrant environ 400 km² et 55 communes. Son réseau de 1 400 stations propose des vélos mécaniques et électriques chargeable directement en borne

Il s'agit d'un jeu de données sur la disponibilité des vélos en libre-service (Vélib') en temps réel en Île-de-France. Nous travaillerons sur un instantané comprenant 1511 stations réparties sur Paris et les communes de la petite couronne. 


#### Dictionnaire de donnée 
Identifiant station : code unique ou code primaire d'identification des stations
Nom station : Libellé de l'emplacement
Station en fonctionnement : c’est l’état de la station  (OUI/NON)
Nombre bornette libre : 
Capacité de la station : Nombre total des bornes
Nombre total vélos disponibles : Somme des vélos mécaniques et électriques
Vélos mécaniques disponibles : Nombre de vélos classiques disponible
Vélos électriques disponibles : Nombre de vélos électrique disponible 
Nom communes équipées : Nom de la commune 
Code INSEE communes équipées : Code administratif de la commune
Coordonnées géographiques : Latitude et Longitude de la station

### Source de donnée

Nos données sont disponible sur le site https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/?disjunctive.is_renting&disjunctive.is_installed&disjunctive.is_returning&disjunctive.name&disjunctive.nom_arrondissement_communes 

### Objectif du projet 

Je vais chercher dans ce projet à visualiser la proportion de vélo électrique par rapport aux vélo mécanique, tout en comparant la disponibilité et l’occupation des stations par commune 
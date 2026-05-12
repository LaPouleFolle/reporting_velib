# reporting_velib
Projet outil de donnée

Vélib’ Métropole est le premier service mondial de vélos en libre-service, couvrant environ 400 km² et 55 communes. Son réseau de 1 400 stations propose des vélos mécaniques et électriques chargeable directement en borne

Il s'agit d'un jeu de données sur la disponibilité des vélos en libre-service (Vélib') en temps réel en Île-de-France. Nous travaillerons sur un instantané comprenant 1511 stations réparties sur Paris et les communes de la petite couronne. 


#### Dictionnaire de donnée 
- Identifiant station - stationcode : code unique ou code primaire d'identification des stations
- Nom station - name : Libellé de l'emplacement
- Station en fonctionnement - is_installed : c’est l’état de la station  (OUI/NON)
- Nombre bornette libre - capacity : 
- Capacité de la station - numdocksavailable: Nombre total des bornes
- Nombre total vélos disponibles - numbikesavailable : Somme des vélos mécaniques et électriques
- Vélos mécaniques disponibles - mechanical : Nombre de vélos classiques disponible
- Vélos électriques disponibles - ebike : Nombre de vélos électrique disponible 
- Nom communes équipées - nom_arrondissement_communes: Nom de la commune 
- occupation_rate : taux d'occupation de la station
- Code INSEE communes équipées - code_insee_commune : Code administratif de la commune
- Coordonnées géographiques - zone : Latitude et Longitude de la station

### Source de donnée

Nos données sont disponible sur le site https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/?disjunctive.is_renting&disjunctive.is_installed&disjunctive.is_returning&disjunctive.name&disjunctive.nom_arrondissement_communes 

### Objectif du projet 

Je vais chercher dans ce projet à visualiser la proportion de vélo électrique par rapport aux vélo mécanique, tout en comparant la disponibilité et l’occupation des stations par commune 
import sys
import json

#1 Charger en mémoire les données issues du fichier JSON reçu en paramètre.

# Le paramètre 0 est le fichier .py en lui même donc les fichiers .json sont les paramètres 1 mais puisqu'on doit loader un ficher à la fois c'est la commande : python EmmyFortin_TP1.py data_small.json ou python EmmyFortin_TP1.py data_large.json qui détermine quel fichier .json est utilisé.

# Récupération du fichier en paramètre (fichier .json soit data_small ou data_large)
json_file = sys.argv[1]

# Chargement des données du ficher .json reçu en paramètre
with open(json_file,"r",encoding="utf-8") as file:
    data = json.load(file)

# Debug pour savoir quel fichier est chargé
print("Fichier chargé :", json_file)



try: 
    print(x)
except NameError: 
    print("X pas défini")
except:
    print("autre")


#2 Détecter les erreurs de chargement de fichier avec try except (et mettre un message d'erreur) QMessageBox.Critical() for error message ( makes a error windows box)

#3 Créer une grille avec Pyside6 qui peut contenir autant d'éléments qu'il y a dans les fichiers JSON (QTableWidget)

#4 Implémenter le tri en ordre croissant et décroissant par colonne.

#5 Fonction de recherche 

#6 Afficher le nom, la taille en mémoire et le nombre d’éléments du fichier

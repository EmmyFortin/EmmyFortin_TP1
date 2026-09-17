from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidget, QLineEdit
import sys
import json

#1 Charger en mémoire les données issues du fichier JSON reçu en paramètre.
#2 Détecter les erreurs de chargement de fichier avec try except (et mettre un message d'erreur) QMessageBox.Critical() for error message ( makes a error windows box)

# Le paramètre 0 est le fichier .py en lui même donc les fichiers .json sont les paramètres 1 mais puisqu'on doit loader un ficher à la fois c'est la commande : python EmmyFortin_TP1.py data_small.json ou python EmmyFortin_TP1.py data_large.json qui détermine quel fichier .json est utilisé.

# Pour détecter les erreurs de chargement de données, il faut mettre un try: il essaye de faire les actions dans sa portée mais s'il n'y arrive pas il passe au execpt
try:
    # Récupération du fichier en paramètre (fichier .json soit data_small ou data_large)
    json_file = sys.argv[1]

    # Chargement des données du ficher .json reçu en paramètre
    with open(json_file,"r",encoding="utf-8") as file:
        data = json.load(file)

    # Debug pour savoir quel fichier est chargé (A SUPPRIMER À LA FIN)
    print("Fichier chargé :", json_file)

# 3 erreures courantes demander si on peut mettre exception au lieu de mettre 3 except
except IndexError:
    print("Erreur index")
    messageIndex = QMessageBox.Critical


except FileNotFoundError:
    print("Fichier non trouvé")

except json.JSONDecodeError:
    print("fichier .json brisé")



#3 Créer une grille avec Pyside6 qui peut contenir autant d'éléments qu'il y a dans les fichiers JSON (QTableWidget)

# Window de base
# QApplication est le ficher correspondant à l'application. C'est donc ce fichier (EmmyFortin_TP1.py) car c'est l'index 0 des argv. Permet l'utilisation des lignes de commandes 
app = QApplication(sys.argv)

# Création du QTableWidget (ma fênetre de tableau)
my_spreadsheet = QTableWidget()
my_spreadsheet.show() # Pour afficher mon tableau car il est caché par défaut

# Boucle d'exécution de l'application
app.exec()

#4 Implémenter le tri en ordre croissant et décroissant par colonne.

#5 Fonction de recherche 

#6 Afficher le nom, la taille en mémoire et le nombre d’éléments du fichier

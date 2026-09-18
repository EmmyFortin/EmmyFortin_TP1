from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidget, QLineEdit, QTableWidgetItem
import sys
import json







# Création d'une class pour créer et afficher la fenêtre qui contiendera la grille
class MainWindow(QMainWindow):
    # __init__ = constructeur qui est appellé automatiquement quand je créer un objet (self = associé à cette fenetre (MainWindow))
    def __init__(self):
        super().__init__()

        # Donne un nom à mon objet MainWindow
        self.setWindowTitle("Gestion de données des fichiers")
        self.create_spreadsheet() 

    # Fonction pour créer et gérer mon tableau (dans la MainWindow) qui peut contenir autant d'éléments que le .JSON en contient
    def create_spreadsheet(self):
        # Permet de créer le tableau dans MainWindow
        self.my_spreadsheet = QTableWidget()
      
        # Détermine le nombre de colonnes et rangée requises pour les données reçu
        self.my_spreadsheet.setColumnCount(8)
        self.my_spreadsheet.setRowCount(8)

        # Place le widget dans ma fenetre
        self.setCentralWidget(self.my_spreadsheet)

        # Appelle la fonction load data
        self.load_data()

    # fonction pour loader le data
    def load_data(self):
        try:
            # Récupération du fichier en paramètre (fichier .json soit data_small ou data_large)
            json_file = sys.argv[1]
           
            # Chargement des données du ficher .json reçu en paramètre
            with open(json_file,"r",encoding="utf-8") as file:
                data = json.load(file)
                # si ca fonctionne
                self.fill_spreadsheet(data)
                print("Fichier chargé :", json_file) # Debug pour savoir quel fichier est chargé (A SUPPRIMER À LA FIN)


            #------------------------------- DEMANDER SI ON PEUT FAIRE UN EXCEPTION 
        except Exception as error: 
            QMessageBox.critical(None, "Erreur", f"Erreur ici:{error} ")
            sys.exit()
        

    # Fonction pour remplir le tableau avec paramètres d'entrés 
    def fill_spreadsheet(self, data):
        self.my_spreadsheet.setRowCount(len(data))
        print(len(data))


# Début de l'application
# Fonction main pour le début de l'application
def main():
    # QApplication est le ficher correspondant à l'application. C'est donc ce fichier (EmmyFortin_TP1.py) car c'est l'index 0 des argv. Permet l'utilisation des lignes de commandes 
    app = QApplication(sys.argv)
    

    # Création de ma fênetre (le constructeur est appellé)
    window = MainWindow()

    # Affichage de ma fenetre car elle est caché par défaut
    window.show()

    # Boucle d'exécution de l'application
    sys.exit(app.exec())

# Indique quand mon programme commence (Si ce ficher est stand alone on appelle la fonction main )
if __name__ == "__main__":
    main()


#1 Charger en mémoire les données issues du fichier JSON reçu en paramètre.
# Le paramètre 0 est le fichier .py en lui même donc les fichiers .json sont les paramètres 1 mais puisqu'on doit loader un ficher à la fois c'est la commande : python EmmyFortin_TP1.py data_small.json ou python EmmyFortin_TP1.py data_large.json qui détermine quel fichier .json est utilisé.
# Pour détecter les erreurs de chargement de données, il faut mettre un try: il essaye de faire les actions dans sa portée mais s'il n'y arrive pas il passe au execpt
try:

    # Récupération du fichier en paramètre (fichier .json soit data_small ou data_large)
    json_file = sys.argv[1]

    # Chargement des données du ficher .json reçu en paramètre
    with open(json_file,"r",encoding="utf-8") as file:
        data = json.load(file)
        


    #print("Fichier chargé :", json_file) # Debug pour savoir quel fichier est chargé (A SUPPRIMER À LA FIN)

#2 Détecter les erreurs de chargement de fichier avec try except (et mettre un message d'erreur) QMessageBox.Critical() for error message ( makes a error windows box)

#------------------------------- DEMANDER SI ON PEUT FAIRE UN EXCEPTION 
except Exception as error: 
    messageError = QMessageBox.critical(None, "Erreur", f"Erreur ici:{error} ")
    sys.exit()

# 3 erreures courantes demander si on peut mettre exception au lieu de mettre 3 except
# except IndexError:
#     messageIndex = QMessageBox.critical(None, "Erreur", "L'index n'est pas valide")
    
# except FileNotFoundError:
#     messageFile = QMessageBox.critical(None,"Erreur","Le fichier est introuvable.")
#     sys.exit()

# except json.JSONDecodeError:
#     messageCode = QMessageBox.critical(None,"Erreur","Le fichier .JSON est invalide.") # Pas de parent direct car on veut montrer qu'il y a une erreur de donnée avant que la grille ouvre (script charge malgré les erreurs dans le .json)
#     sys.exit()

# ---------------------------DEMANDER POUR LE COMPORTEMENT APRÈS AVOIR EU LE MESSAGE D'ERREUR

#----- SI PROF VEUT QU'ON FERME LE PROGRAMME MANUELLEMENT ET QU'ON CORRIGE L'ERREUR MANUELLEMENT DANS .JSON :

#3 Créer une grille avec Pyside6 qui peut contenir autant d'éléments qu'il y a dans les fichiers JSON (QTableWidget)
# Création du QTableWidget (ma fênetre de tableau)




#my_spreadsheet = QTableWidget(1,8)
# Affichage de mon tableau car il est caché par défaut
#my_spreadsheet.show() 

# # Boucle d'exécution de l'application
#sys.exit(app.exec())

#----- SI PROF VEUT QU'ON BYPASS L'ERREUR ET QU'ON OUVRE QUAND MEME LE TABLEAU (ON PRÉCISE L'ÉLÉMENT IGNORÉ ):
# Création d'une liste vide des données valides (------------------Je mets tu juste les éléments  qu'il demande d'afficher dans le tableau (nom, taille et quantité d'éléments) ou je met tout ?)
# valid_data = []

# for element in data:
#     if(
#         "id" in element
#         and "nom" in element
#         and "categorie" in element
#         and "format" in element
#         and "polygones" in element
#         and "statut" in element
#         and "auteur" in element
#         and "date_creation" in element
#         and "prix" in element
#         and "taille_fichier" in element
#     ):
#         #Ajoute les éléments valide dans la liste vide de valid_data
#         valid_data.append(element)

#     else:
#         print("Élément invalide ignoré :", element)
    # FAIRE OUVRIR FENETRE AVEC DONNÉES VALIDES   

#4 Implémenter le tri en ordre croissant et décroissant par colonne.

#5 Fonction de recherche 

#6 Afficher le nom, la taille en mémoire et le nombre d’éléments du fichier

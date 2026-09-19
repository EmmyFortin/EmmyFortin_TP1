from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidget, QLineEdit, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QMargins
import sys
import json


# Création d'une class pour créer et afficher la fenêtre qui contiendera la grille
class MainWindow(QMainWindow):
    # __init__ = constructeur qui est appellé automatiquement quand je créer un objet (self = associé à cette fenetre (MainWindow))
    def __init__(self):
        super().__init__()

        # Donne un nom à mon objet MainWindow
        self.setWindowTitle("Gestion de données des fichiers")

        # Appelle la fonction create spreadsheet 
        self.create_spreadsheet() 

    # Fonction pour créer et gérer mon tableau (dans la MainWindow) qui peut contenir autant d'éléments que le .JSON en contient
    def create_spreadsheet(self):

        # Permet de créer le tableau dans MainWindow
        self.my_spreadsheet = QTableWidget()

        # Titre pour les boutons de tri
        self.sorting_title = QLabel("Sort by")

        # Création des boutons pour trier les données en ordre croissant et décroissant qui appelle leur fonction de tri
        self.ascending_button = QPushButton("Ascending order")
        #action du bouton

        self.descending_button = QPushButton("Descending order")
        # action du bouton

        # QHBoxLayout place les widgets à l'horizontal
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.sorting_title)
        filters_layout.addWidget(self.ascending_button)
        filters_layout.addWidget(self.descending_button)

        # QVBox Layout place les widgets à la verticale
        layout = QVBoxLayout()
        layout.addLayout(filters_layout)
        layout.addWidget(self.my_spreadsheet)

        # Le container contient tout les widgets
        container = QWidget()
        container.setLayout(layout)

        # Donne les valeurs pour les margins de la fênetre
        margins = QMargins(4,10,4,10)
        self.setContentsMargins(margins)

        # Place le widget dans ma fenetre
        self.setCentralWidget(container)

        # Appelle la fonction load data
        self.load_data()

    #1 Charger en mémoire les données issues du fichier JSON reçu en paramètre.
    # Fonction pour charger les données du fichier JSON
    def load_data(self):
        # Pour détecter les erreurs de chargement de données, il faut mettre un try: il essaye de faire les actions dans sa portée mais s'il n'y arrive pas il passe au execpt
        try:
            # Récupération du fichier en paramètre (fichier .json soit data_small ou data_large)
            # Le paramètre 0 est le fichier .py en lui même donc les fichiers .json sont les paramètres 1 mais puisqu'on doit loader un ficher à la fois c'est la commande : python EmmyFortin_TP1.py data_small.json ou python EmmyFortin_TP1.py data_large.json qui détermine quel fichier .json est utilisé.
            json_file = sys.argv[1]
           
            # Chargement des données du ficher .json reçu en paramètre
            with open(json_file,"r",encoding="utf-8") as file:
                assets_data = json.load(file) # assets_data = contenu du fichier .json
                print("Fichier chargé :", json_file) # Debug pour savoir quel fichier est chargé (A SUPPRIMER À LA FIN)

            # Récupérer les keys (nom des propriétés des assets) pour les afficher en tant que label pour chaque colonne
            # Création d'une liste qui va contenir le nom des colonnes (nom des propriétés des assets)
            column_names = []

            # Pour chaque asset (objet) dans le fichier .json loadé on cherche le nom chaque propriété de l'asset ("id", "name", etc) si le nom de la propriété n'est pas déjà dans la liste des noms des colonnes on l'ajoute. À la fin de la boucle column_name contient le nom de toute les propriétes des assets
            for asset in assets_data:
                for property_name in asset:
                    if property_name not in column_names:
                        column_names.append(property_name)

            # Appelle la fonction pour remplir le tableau
            self.fill_spreadsheet(assets_data, column_names)


        #2 Détecter les erreurs de chargement de fichier avec try except (et mettre un message d'erreur) QMessageBox.Critical() for error message ( makes a error windows box)

        #--------------- 3 erreures courantes demander si on peut mettre exception au lieu de mettre 3 except
        # except IndexError:
        #     messageIndex = QMessageBox.critical(None, "Erreur", "L'index n'est pas valide")
            
        # except FileNotFoundError:
        #     messageFile = QMessageBox.critical(None,"Erreur","Le fichier est introuvable.")
        #     sys.exit()

        # except json.JSONDecodeError:
        #     messageCode = QMessageBox.critical(None,"Erreur","Le fichier .JSON est invalide.") # Pas de parent direct car on veut montrer qu'il y a une erreur de donnée avant que la grille ouvre (script charge malgré les erreurs dans le .json)
        #     sys.exit()

        #------------------------------- DEMANDER SI ON PEUT FAIRE UN EXCEPTION 

        except Exception as error: 
            QMessageBox.critical(None, "Erreur", f"Erreur ici:{error} ")
            sys.exit()

        # ---------------------------DEMANDER POUR LE COMPORTEMENT APRÈS AVOIR EU LE MESSAGE D'ERREUR
            # Option 1 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme se ferme (sys.exit). Je dois donc corriger mannuellement le problème dans le .json
            # Option 2 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme ne se ferme pas (pas de sys.exit) mais le tableau est vide (fill spreadsheet est pas appeler)
            # Option 3 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme ne se ferme pas et le tableau load et précise qu'un élément est ignoré (je dois ajouter une vérification des donnée dans le try )
       

    # Fonction pour remplir le tableau avec paramètres d'entrés 
    def fill_spreadsheet(self, assets_data, column_names):

        # On met le nombre de rangés équivalente à au nombre (lenght) des données
        self.my_spreadsheet.setRowCount(len(assets_data))

        # On met le nombre de colonnes équivalente à au nombre (lenght) des données
        self.my_spreadsheet.setColumnCount(len(column_names))

        # On met les Labels des colonnes (correspond aux noms des keys)
        self.my_spreadsheet.setHorizontalHeaderLabels(column_names)



        # Afficher les données dans le tableau

        # enumerate a besoin d'être effectué en priorité (avant le for loop) pour que la boucle sache sur quoi elle va looper (variables row_index et current_asset on pas encore eu de valeur)
        # enumerate parcourt tout les éléments(assets) dans assets_data (contenu du .json) et donne un index à chaque asset. 
        # Le résultat du enumerate fourni à chaque tour une paire de donnée ex: row_index = 0 et current_asset = asset1, row_index = 1 et current_asset = asset2 etc.
        # Le for loop parcourt les paires une par une
        # À chaque tour, l'index qu'il(enumrate) fournit est stocké dans row_index et l'asset correspondant (à cet index) est stocké dans current_asset
         
        for row_index, current_asset in enumerate(assets_data):
           
            # enumerate parcourt tout les noms des colonnes dans la liste column_names et donne un index à chacun
            # Le résultat du enumerate fourni à chaque tour une paire de donnée
            # Le for loop parcout les paires une par une
            # À chaque tour, l'index qu'il(enumerate) fournit est stocké dans column_index et le nom de la colonne correspondant (à cet index) est stocké dans current_column_name

            for column_index, current_column_name in enumerate(column_names):

                # On stocke la valeur de la propriété(id, name etc.) de l'asset parcouru qui correspond au nom de la colonne parcourue ( "id", "name" etc.).
                cell_value = current_asset[current_column_name]

                # Converti la valeur de cell_value en string et création d'un QTableWidgetItem pour que la valeur puisse être afficher dans le tableau
                spreadsheet_item = QTableWidgetItem(str(cell_value))

                # Permet de placer le QTableWidgetItem dans le tableau à la rangée et à la colonne présemtent parcourue
                self.my_spreadsheet.setItem(row_index, column_index, spreadsheet_item)

        # Pour que le tableau s'adapte à la taille du contenu des colonnes et des rangées
        # Je veux un display parfait à l'ouverture du tableau
        # Calcul qui addition la largeur (h) des headers de mes colonnes avec la longueur (v) des headers de mes rangées avec l'épaisseur de la bordure exterieur du tableau qui est multiplié par deux (pour gauche et droite)
        spreadsheet_width = (
            self.my_spreadsheet.horizontalHeader().length()
            + self.my_spreadsheet.verticalHeader().width()
            + self.my_spreadsheet.frameWidth() * 2
        )

        # Pour enlever la scroll bar horizontal qui est présent dans le grand tableau (à cause de la scroll bar vertical)
        if self.my_spreadsheet.verticalScrollBar().maximum() > 0:
            spreadsheet_width += self.my_spreadsheet.verticalScrollBar().sizeHint().width()

        self.my_spreadsheet.setMinimumWidth(spreadsheet_width)
        self.adjustSize()




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





#4 Implémenter le tri en ordre croissant et décroissant par colonne.

#5 Fonction de recherche 

#6 Afficher le nom, la taille en mémoire et le nombre d’éléments du fichier

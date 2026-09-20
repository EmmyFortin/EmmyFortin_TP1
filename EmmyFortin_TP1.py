from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import QMargins, Qt, QFileInfo
import sys
import json

# Création d'une classe pour la fenêtre principale de l'application dans
# laquelle tous les widgets seront ajoutés et affichés.


class MainWindow(QMainWindow):
    """"Représente la fenêtre principale de l'application."""


    # __init__ = constructeur qui est appelé automatiquement quand je crée un objet. 
    # self = associé à cette fenêtre (MainWindow).
    def __init__(self):
        """Initialise la fenêtre principale de l'application."""
        # Appelle le constructeur de la classe parent QMainWindow.
        super().__init__()

        # Donne un nom à mon objet MainWindow
        self.setWindowTitle("Gestion de données des fichiers")

        # Appelle la fonction create spreadsheet
        self.create_spreadsheet()

    # Fonction pour créer et gérer mon tableau (dans la MainWindow) qui peut 
    # contenir autant d'éléments que le .JSON en contient
    def create_spreadsheet(self):
        """Crée et configure le tableau qui est dans la fenêtre principale."""

        # Permet de créer le tableau dans MainWindow
        self.my_spreadsheet = QTableWidget()

        # Titre pour les boutons de tri
        self.sorting_title = QLabel("Trier les Ids par")

        # Création des boutons pour trier les données en ordre croissant et 
        # décroissant qui appelle leur fonction de tri après un click
        self.ascending_button = QPushButton("Ordre Ascendant")
        self.ascending_button.clicked.connect(self.sort_by_ascending)

        self.descending_button = QPushButton("Ordre Descendant")
        self.descending_button.clicked.connect(self.sort_by_descending)

        # Création des textes de bas de page pour les informations du fichier
        self.displayed_file_name = QLabel()
        self.file_size_in_memory = QLabel()
        self.number_of_elements = QLabel()

        # QHBoxLayout place les widgets à l'horizontal
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.sorting_title)
        filters_layout.addWidget(self.ascending_button)
        filters_layout.addWidget(self.descending_button)

        # Création de la barre de recherche 
        # (QLineEdit permet d'éditer le texte)
        searchbar = QLineEdit(placeholderText="Rechercher...")
        searchbar.textChanged.connect(self.update_search)

        # QVBox Layout place les widgets à la verticale
        layout = QVBoxLayout()
        layout.addWidget(searchbar)
        layout.addLayout(filters_layout)
        layout.addWidget(self.my_spreadsheet)
        layout.addWidget(self.displayed_file_name)
        layout.addWidget(self.file_size_in_memory)
        layout.addWidget(self.number_of_elements)

        # Le container contient tout les widgets
        container = QWidget()
        container.setLayout(layout)

        # Donne les valeurs pour les margins de la fênetre
        margins = QMargins(4, 10, 4, 10)
        self.setContentsMargins(margins)

        # Place le widget dans ma fenetre
        self.setCentralWidget(container)

        # Appelle la fonction load data
        self.load_data()


    # Fonction pour charger les données du fichier JSON
    def load_data(self):
        """Charge en mémoire les données du fichier JSON reçu en paramètre"""
        # Pour détecter les erreurs de chargement de données, il faut mettre un try
        # Le try essaye d'exécuter les actions dans sa portée. 
        # S'il n'y arrive pas il passe au execpt
        try:
            # Récupération du fichier JSON reçu en paramètre.
            # Le paramètre 0 est le fichier .py en lui même.
            # Le paramètre 1 est le fichier JSON reçu en paramètre.
            # Puisqu'on doit charger un ficher à la fois, 
            # la commande suivante détermine quel fichier JSON est utilisé : 
            # python EmmyFortin_TP1.py data_small.json 
            # ou 
            # python EmmyFortin_TP1.py data_large.json 
            json_file = sys.argv[1]

            # Chargement des données du ficher .json reçu en paramètre
            with open(json_file, "r", encoding="utf-8") as file:
                assets_data = json.load(file)  # assets_data = contenu du fichier JSON

            # Récupere les informations du fichier pour pouvoir les afficher
            # dans le bas de la fênetre
            file_infos = QFileInfo(json_file)

            # Récupère le nom du fichier chargé, sa taille en mémoire 
            # et son nombre d'éléments
            file_name = file_infos.fileName()
            file_size = sys.getsizeof(assets_data)
            file_elements = len(assets_data)

            # Mettre les infos dans les QLabels
            self.displayed_file_name.setText(
                f"Nom du fichier chargé : {file_name}"
            )
            self.file_size_in_memory.setText(
                f"Taille du fichier en mémoire : {file_size} bytes"
            )
            self.number_of_elements.setText(
                f"Nombre d'éléments du fichier : {file_elements}"
            )

            # Récupérer les keys (nom des propriétés des assets) pour les afficher 
            # en tant que labels pour chaque colonne.
            # Création d'une liste qui va contenir le nom des colonnes
            # (nom des propriétés des assets).
            column_names = []

            # Pour chaque asset (objet) dans le fichier JSON chargé, on cherche le nom
            # de chaque propriété de l'asset ("id", "name", etc). 
            # Si le nom de la propriété n'est pas déjà dans la liste des noms de
            # colonne on l'ajoute. À la fin de la boucle, column_names contient
            # le nom de toute les propriétes des assets.
            for asset in assets_data:
                for property_name in asset:
                    if property_name not in column_names:
                        column_names.append(property_name)

            # Appelle la fonction pour remplir le tableau
            self.fill_spreadsheet(assets_data, column_names)



        # --------------- 3 erreures courantes demander si on peut mettre exception au lieu de mettre 3 except
        # except IndexError:
        #     messageIndex = QMessageBox.critical(None, "Erreur", "L'index n'est pas valide")

        # except FileNotFoundError:
        #     messageFile = QMessageBox.critical(None,"Erreur","Le fichier est introuvable.")
        #     sys.exit()

        # except json.JSONDecodeError:
        #     messageCode = QMessageBox.critical(None,"Erreur","Le fichier .JSON est invalide.") # Pas de parent direct car on veut montrer qu'il y a une erreur de donnée avant que la grille ouvre (script charge malgré les erreurs dans le .json)
        #     sys.exit()

        # ------------------------------- DEMANDER SI ON PEUT FAIRE UN EXCEPTION



        # Si une erreur survient lors du chargement des données, elle est stockée
        # dans la variable error.
        # Une fenêtre s'ouvre et affiche le message d'erreur.
        # Puis l'application se ferme quand on appuis sur OK.
        
        # None est utilisé car il n'y a pas de parent direct associé au QMessageBox.
        # Le message d'erreur doit pouvoir s'afficher même si la 
        # fenêtre principale n'a pas pu être chargée correctement
        except Exception as error:
            QMessageBox.critical(
                None,
                "Erreur de chargement",
                f"Impossible de charger les données du fichier JSON.\n\n"
                f"Détails de l'erreur : {error}"
            )
            sys.exit()



        # ---------------------------DEMANDER POUR LE COMPORTEMENT APRÈS AVOIR EU LE MESSAGE D'ERREUR
        # Option 1 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme se ferme (sys.exit). Je dois donc corriger mannuellement le problème dans le .json
        # Option 2 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme ne se ferme pas (pas de sys.exit) mais le tableau est vide (fill spreadsheet est pas appeler)
        # Option 3 Quand ya une erreur je vois le message et je fais ok sur le message -> le programme ne se ferme pas et le tableau load et précise qu'un élément est ignoré (je dois ajouter une vérification des donnée dans le try )



    # Fonction pour remplir le tableau avec les paramètres d'entrée.
    def fill_spreadsheet(self, assets_data, column_names):
        """Remplit le tableau avec les données des assets et les noms de colonnes."""

        # Donne le nombre de rangés par rapport au nombre (lenght) d'assets.
        self.my_spreadsheet.setRowCount(len(assets_data))

        # Donne le nombre de colonnes par rapport au nombre (lenght) de noms de colonnes.
        self.my_spreadsheet.setColumnCount(len(column_names))

        # Donne les Labels des colonnes (correspond aux noms des keys)
        self.my_spreadsheet.setHorizontalHeaderLabels(column_names)

        # Afficher les données dans le tableau
        # La première boucle parcourt une rangée (un asset) à la fois.
        # Pour chaque rangée, la deuxième boucle parcourt toutes ses colonnes.
        # Une fois toutes les colonnes parcourues, la première boucle passe à la
        # rangée suivante et le processus recommence.

        # enumerate doit d'être effectué avant la for loop pour que celle-ci sache sur 
        # quoi elle va looper. Les variables row_index et current_asset n'ont pas encore de valeur.
        # enumerate parcourt tous les éléments (assets) dans assets_data (contenu
        # du fichier JSON) et donne un index à chaque asset.
        # Le résultat du enumerate fourni à chaque tour une paire de donnée, 
        # ex: row_index = 0 et current_asset = asset1,
        #     row_index = 1 et current_asset = asset2, etc.
        # La for loop parcourt les paires une par une.
        # À chaque tour de la for loop, l'index fournit par enumerate est stocké dans row_index
        # et l'asset correspondant à cet index est stocké dans current_asset.

        for row_index, current_asset in enumerate(assets_data):

            
            # Même principe que pour les rangées, enumerate parcourt les colonnes (column_names)
            # et récupère leur index et leur nom

            for column_index, current_column_name in enumerate(column_names):

                # On stocke la valeur de la propriété(id, name etc.) de l'asset 
                # parcouru qui correspond au nom de la colonne parcourue.
                cell_value = current_asset[current_column_name]

                # Converti la valeur de cell_value en string.
                # Création d'un QTableWidgetItem pour que la valeur puisse être affiché dans le tableau.
                spreadsheet_item = QTableWidgetItem(str(cell_value))

                # Permet de placer le QTableWidgetItem dans le tableau à la rangée et à la colonne
                # présentement parcourue
                self.my_spreadsheet.setItem(
                    row_index, 
                    column_index, 
                    spreadsheet_item
                )

        # Place par défaut les éléments par ordre croissant selon leur id, même si 
        # leur ordre est différent dans le JSON (ex: on met le NAND403-003 avant le NAND403-002).
        self.sort_by_ascending()

        # Active le tri par colonne
        self.my_spreadsheet.setSortingEnabled(True)

        # Adapte la largeur du tableau à la taille de son contenu pour avoir un
        # affichage complet dès l'ouverture.
        # Calcul qui additionne la longueur (h) des headers des colonnes, 
        # la largeur (v) des headers des rangées et
        # l'épaisseur de la bordure exterieur du tableau multiplié par deux (gauche et droite)
        spreadsheet_width = (
            self.my_spreadsheet.horizontalHeader().length()
            + self.my_spreadsheet.verticalHeader().width()
            + self.my_spreadsheet.frameWidth() * 2
        )


        # Si une scrollbar verticale est présente, on ajoute sa largeur
        # afin d'éviter l'apparition d'une scrollbar horizontale.

        # On récupère la scrollbar verticale de QTableWidget et on vérifie 
        # son maximum. S'il est supérieur à 0, il y a du défilement vertical.
        if self.my_spreadsheet.verticalScrollBar().maximum() > 0:

            # sizeHint() demande à Qt la taille recommandée pour la scrollbar
            # et width() récupère seulement la largeur de cette taille.
            spreadsheet_width += (
                self.my_spreadsheet.verticalScrollBar().sizeHint().width()
            )

        self.my_spreadsheet.setMinimumWidth(spreadsheet_width)
        self.adjustSize()

    # Fonction pour trier par id  le 0 correspond à l'index de la colonne qui contient les ids
    # Tri en ordre croissant
    def sort_by_ascending(self):
        self.my_spreadsheet.sortItems(0, Qt.AscendingOrder)

    # Tri en ordre décroissant
    def sort_by_descending(self):
        self.my_spreadsheet.sortItems(0, Qt.DescendingOrder)

    # Fonction de recherche et d'autocomplétion
    def update_search(self, text):
        # Permet d'effacer le vieux texte et récupère ce que j'écris tout en ignorant les maj/min
        searched_text = text.strip().casefold()

        # rowCount determine le nombre de rangées dans mon tableau actuellement
        number_of_rows = self.my_spreadsheet.rowCount()

        number_of_columns = self.my_spreadsheet.columnCount()

        # Boucle qui permet de parcourir toutes les rangées de mon tableau une par une
        # Le range renvoye une suite de nombres. Par défaut les nombres commence à 0 puis s'incrémente de 1 et s'arrete avant un chiffre spécifier (valeur de number_of_rows).
        # En gros, range indique combien de fois il faut looper dans row
        # à chaque tour, le numéro de la rangée parcouru est stocké dans row
        for row in range(number_of_rows):

            # Variable pour contenir le texte présent dans la rangée parcourue
            row_content = ""

            # Boucle qui permet de parcourir toutes les colonnes de mon tableau une par une
            # Même principe ici
            for column in range(number_of_columns):
                cell = self.my_spreadsheet.item(row, column)
                row_content += cell.text().casefold()

            # Si le texte qu'on cherche est présent dans la rangé on affiche la rangé
            if searched_text in row_content:
                self.my_spreadsheet.showRow(row)

            # sinon on cache la rangé
            else:
                self.my_spreadsheet.hideRow(row)


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

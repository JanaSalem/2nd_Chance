# Description du fichier : item.py

class Item:
    """
    Classe représentant un objet que le joueur peut trouver dans les pièces du jeu.

    Attributs :
        - name : str : le nom de l'objet
        - description : str : la description de l'objet
        - weight : float : le poids de l'objet (en kilogrammes)

    Méthodes :
        - __str__() : retourne une représentation textuelle de l'objet.
    """

    def __init__(self, name, description, weight):
        """
        Initialise un nouvel objet Item.

        Args:
            name (str): Le nom de l'objet.
            description (str): La description de l'objet.
            weight (float): Le poids de l'objet en kilogrammes.
        """
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """
        Redéfinition de la méthode __str__ pour retourner une représentation textuelle
        de l'objet avec son nom, description et poids.

        Returns:
            str: Représentation textuelle de l'objet.
        """
        return f"Item(name={self.name}, description{self.description}, weight{self.weight} kg)"


"""
Module Item

Ce module définit la classe `Item`, qui représente un objet manipulable dans le jeu.
"""
class Item:
    """
    Classe représentant un objet dans le jeu.
    
    Attributs:
    ----------
    name : str
        Le nom de l'objet.
    description : str
        La description détaillée de l'objet.
    weight : float
        Le poids de l'objet en kilogrammes.
    
    Méthodes:
    --------
    __init__(name, description, weight):
        Initialise un nouvel objet avec un nom, une description et un poids.
    __str__():
        Retourne une représentation textuelle de l'objet sous forme de chaîne.
    """

    def __init__(self, name: str, description: str, weight: float):
        """
        Initialise un objet Item avec les attributs donnés.

        Paramètres:
        -----------
        name : str
            Le nom de l'objet.
        description : str
            La description détaillée de l'objet.
        weight : float
            Le poids de l'objet en kilogrammes.
        """
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet.

        Exemple de sortie:
        "sword : une épée au fil tranchant comme un rasoir (2 kg)"
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"

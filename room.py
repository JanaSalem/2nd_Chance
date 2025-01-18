"""Module définissant les pièces du jeu d'aventure.

Ce module contient la classe Room qui représente les différentes pièces
du jeu, leurs connexions et leur contenu.
"""

from PIL import Image


class Room:
    """Classe représentant une pièce dans le jeu d'aventure.

    Cette classe gère les attributs et comportements d'une pièce, incluant
    sa description, ses sorties, son inventaire et les personnages présents.

    Attributes:
        name (str): Nom de la pièce.
        description (str): Description détaillée de la pièce.
        exits (dict): Dictionnaire des sorties disponibles.
        inventory (dict): Inventaire des objets présents dans la pièce.
        characters (dict): Dictionnaire des personnages présents.
        visited (bool): Indique si la pièce a été visitée.
        image_path (str): Chemin vers l'image associée à la pièce.
    """

    def __init__(self, name: str, description: str, exits: dict):
        """Initialise une nouvelle pièce.

        Args:
            name (str): Nom de la pièce.
            description (str): Description de la pièce.
            exits (dict): Dictionnaire initial des sorties.
        """
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
        self.visited = False
        self.image_path = None

    def get_exit(self, direction: str) -> 'Room':
        """Retourne la pièce accessible dans la direction donnée.

        Args:
            direction (str): Direction souhaitée.

        Returns:
            Room: Pièce dans la direction donnée ou None si pas de sortie.
        """
        return self.exits.get(direction)

    def get_exit_string(self) -> str:
        """Retourne une description des sorties disponibles.

        Returns:
            str: Liste formatée des sorties disponibles.
        """
        available_exits = [exit_dir for exit_dir, room in self.exits.items()
                         if room is not None]
        return "Sorties: " + ", ".join(available_exits)

    def get_long_description(self) -> str:
        """Retourne une description détaillée de la pièce.

        Returns:
            str: Description incluant la pièce et ses sorties.
        """
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"

    def add_item(self, item) -> None:
        """Ajoute un objet à l'inventaire de la pièce.

        Args:
            item: Objet à ajouter à l'inventaire.
        """
        self.inventory[item.name] = item

    def remove_item(self, item_name: str) -> None:
        """Retire un objet de l'inventaire de la pièce.

        Args:
            item_name (str): Nom de l'objet à retirer.
        """
        self.inventory.pop(item_name, None)

    def add_character(self, character) -> None:
        """Ajoute un personnage à la pièce.

        Args:
            character: Personnage à ajouter à la pièce.
        """
        self.characters[character.name.lower()] = character

    def show_image(self) -> None:
        """Affiche l'image associée à la pièce si elle existe."""
        if not self.image_path:
            return

        try:
            img = Image.open(self.image_path)
            img.show()
        except Exception as error:
            print(f"Erreur lors de l'affichage de l'image : {error}")

    def print_inventory(self) -> None:
        """Affiche le contenu de l'inventaire de la pièce."""
        if not self.inventory:
            print("vide")
            return

        print("\nOn voit :")
        for item in self.inventory.values():
            print(f"   {item.name} : {item.description}")

    def print_description(self) -> None:
        """Affiche la description de la pièce."""
        print(self.description)

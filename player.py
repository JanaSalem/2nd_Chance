"""
Fichier player.py

Ce fichier définit la classe Player et ses méthodes associées pour le jeu d'aventure.
Il gère les interactions comme l'historique, la manipulation d'item et d'inventory.
"""
class Player():
    """Classe qui represente joueur du jeu.

    Attributes:
        name (str)
        current_room (str)
        history (lst)
        inventory (dict)
    """

    # Define the constructor.
    def __init__(self, name):
        """
        Initialise les attributs de base pour un nouvel objet Game.
        """
        self.name = name
        self.current_room = None
        self.history = []  # Historique des pièces visitées 🌸
        self.inventory = {}

    #🌸
    def undo(self):
        """"Configure le undo"""
        if self.history:
            # Reviens à la dernière pièce dans l'historique
            self.current_room = self.history.pop()
            print(self.current_room.get_long_description())
        else:
            print("\nAucun retour en arrière possible.\n")

    def get_history(self):
        """# Vérifie si l'historique est vide
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres pièces.\n"
        
        # Crée une chaîne de caractères pour l'historique des pièces visitées
        history_str = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in self.history:
            history_str += f"\t- {room.description}\n"
        
        return history_str"""

        #donne l'historique des pieces visitées par le joueur
        if len(self.history)==0:
            print ( "Vous n'avez visiter aucune pièce")
            return False
        else:
            print("Vous avez visité les piéces: ")
            for room in self.history:
                print(room.name)
            return True


    def add_item(self, item):
        """Ajoute un item à l'inventaire du joueur."""
        self.inventory[item.name] = item


    def print_inventory(self):

        """if len(self.inventory) == 0:
            print("Votre inventaire est vide.")
            return True
        
        print("\nVous disposez des items suivants :\n")
        for key, value in self.inventory.items():
            print("-" + key + " : " + str(self.inventory[key]))
            #print(key.name, ":", key)
        return True"""

        #donne l'inventaire du joueur
        if  not self.inventory:
            print("Votre inventaire est vide")
            return
        else :
            for key ,item in self.inventory.items():
                print("vous avez dns votre inventaire:\n", item,)


    # Define the move method.
    def move(self, direction):
        """Configuration du mouve"""
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        self.history.append(self.current_room)
        # Set the current room to the next room.
        self.current_room = next_room
        Player.get_history(self)

        return True
    
    
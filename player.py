# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        

        self.name = name
        self.current_room = None
        self.history = []  # Historique des pièces visitées 🌸
        self.inventory = {}
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Ajoute la pièce actuelle dans l'historique 🌸
        self.history.append(self.current_room)

        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())

        # Ajoute la pièce actuelle dans l'historique 🌸
        print(self.get_history()) 

        return True
    
    #🌸
    def undo(self):
        if self.history:
            # Reviens à la dernière pièce dans l'historique
            self.current_room = self.history.pop()
            print(self.current_room.get_long_description())
        else:
            print("\nAucun retour en arrière possible.\n")

    def get_history(self):
        # Vérifie si l'historique est vide
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres pièces.\n"
        
        # Crée une chaîne de caractères pour l'historique des pièces visitées
        history_str = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in self.history:
            history_str += f"\t- {room.description}\n"
        
        return history_str
    


    #🌸
    def add_item(self, item):
        """
        Ajoute un item à l'inventaire du joueur.
        
        Paramètres:
        item : Item
            L'objet à ajouter dans l'inventaire.
        """
        self.inventory[item.name] = item

    def remove_item(self, item_name):
        """
        Retire un item de l'inventaire du joueur.
        
        Paramètres:
        item_name : str
            Le nom de l'objet à retirer.
        """
        if item_name in self.inventory:
            del self.inventory[item_name]

    def get_inventory(self):
        """
        Affiche tous les objets dans l'inventaire du joueur.
        """
        if not self.inventory:
            print("Votre inventaire est vide.")
        else:
            for item in self.inventory.values():
                print(item)

    

    


    
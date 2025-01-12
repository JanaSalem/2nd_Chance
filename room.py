# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory_room = set() #room🌟
        self.characters = {}
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
    

    # Ajouter un objet à l'inventaire de la pièce
    def add_item(self, item):
        self.inventory_room[item.name] = item

    def remove_item(self, item_name):
        if item_name in self.inventory_room:
            del self.inventory_room[item_name]

    # Ajouter un personnage à la pièce
    def add_character(self, character):
        self.characters[character.name.lower()] = character  # Utilisation de .lower() pour les comparaisons insensibles à la casse



    def print_inventory_room(self): #room 🌟
        if len(self.inventory_room) == 0:
            print("Ce lieu ne contient aucun item : L'inventaire est vide.")
            return True
        
        print("\nLa pièce contient :\n")
        for i in self.inventory_room:
            print("   ", i.name, ":", i.description)

        if self.characters:
            print("\nVous remarquez également :")
            for character in self.characters.values():
                print(f"    {character.name} : {character.description}")
            
        return True

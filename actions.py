import os
from PIL import Image

#from config import DEBUG
# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        if direction in player.current_room.exits:
            # Move the player in the direction specified by the parameter.
            player.move(direction)
            player.current_room.visited = True #???
            # Afficher la description de la pièce actuelle
            print(player.current_room.description)
            #Affiche description de la pièce actuelle
            if not player.current_room.visited:
                player.current_room.show_image()
            print(f"\nSorties: {', '.join(player.current_room.exits.keys())}\n")

            
        else:
            print("Direction non valide veuillez réessayer")
        return True

        """if direction not in player.current_room.exits:
            print(f"\nIl n'y a pas de sortie dans la direction {direction}.")
        return False
        # Move the player in the direction specified by the parameter.
        sucess = player.move(direction)
        if not sucess:
            return False"""
        
        # Afficher la description de la pièce actuelle
        """print(player.current_room.description)
        print(f"\nSorties: {', '.join(player.current_room.exits.keys())}\n")

        # Affichage des personnages dans la pièce
        if player.current_room.characters:
            for character in player.current_room.characters.values():
                print(f"Vous voyez {character.name} ici : {character.description}")

        return True"""



        """for character in player.current_room.characters.values():  # Corrected line
            #if character.current_room == player.current_room:
            print(f"Vous voyez {character.name} ici : {character.description}")
            return True 

        # Afficher les sorties disponibles
        print(f"\nSorties: {', '.join(player.current_room.exits.keys())}\n")
        return True"""

        """if DEBUG:
            print(f"DEBUG: Le joueur {player.name} s'est déplacé vers {direction}.")

        # Afficher les personnages dans la pièce du joueur si DEBUG est activé
        if DEBUG:
            print("DEBUG: Vérification des personnages dans la nouvelle pièce...")
    
        for character in player.current_room.characters.values():  # Itérer sur les valeurs du dictionnaire
            if character.current_room == player.current_room:
                print(f"DEBUG: Vous voyez {character.name} ici : {character.description}")
    
        return True"""

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    #🌸
    def back(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de revenir à la dernière pièce visitée.
        """
        player = game.player
        """# Vérifiez si l'historique n'est pas vide
        if len(player.history) > 0:
            # Retirer la dernière pièce de l'historique et définir cette pièce comme la pièce actuelle
            last_room = player.history.pop()
            player.current_room = last_room
            print(f"\nVous revenez dans la pièce précédente : {last_room.name}")
            print(last_room.get_long_description())
            print(player.get_history())  # Affiche l'historique des pièces visitées
            return True
        else:
            # Si l'historique est vide, le joueur ne peut pas revenir en arrière
            print("\nIl n'y a aucune pièce précédente dans l'historique.")
            return False"""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        #cas dans lequel le joueur est dans la piece de départ
        if player.history == []:
            print ("Vous etes a la case de départ")
            return False
        else:
            room=player.history.pop()
            player.current_room= room
            player.get_history()
            print(player.current_room.get_long_description())
            return True
    
        
    def check(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        player=game.player
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
    
        game.player.print_inventory()
        return True

    def look(game, list_of_words, number_of_parameters):
        """l = len(list_of_words)
        if l != number_of_parameters + 1:      #le joueur n'a pas correctement saisi la commande.
            command_word = list_of_words[0]
            print(MSG0.format(command_word = command_word))
            return False
   
        game.player.current_room.print_inventory()
        return True"""
        # Permet d'identifié les items et pnj présents dans la pièce  
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        game.player.current_room.print_inventory()
        #print(game.player.current_room.get_long_description())
        return True
    
    def take(game, list_of_words, number_of_parameters):
        """l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
   
        item_choisi = list_of_words[1]  # 🌟 Récupère le nom de l'objet à prendre. j ai fait comme ju 
        for i in game.player.current_room.inventory_room:
            if i.name == item_choisi : 
                game.player.inventory[i]=i
                game.player.current_room.inventory_room.remove(i)
                print("\nCette item a été ajouté à votre inventaire !")
                return True

        print("Cette item n'existe pas")

        # Vérifie si l'objet existe dans la pièce actuelle
        item = self.current_room.inventory.get(item_name)
    
        if not item:
            print(f"\nIl n'y a pas d'objet nommé '{item_name}' dans cette pièce.")
            return
    
        # Ajoute l'objet à l'inventaire du joueur
        self.player.add_item(item)
        # Retire l'objet de la pièce (ou le met dans l'inventaire de la pièce)
        del self.current_room.inventory[item_name]
        print(f"\nVous avez pris l'objet '{item_name}'.")"""
        
        l = len(list_of_words)
        player=game.player
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        if list_of_words[1] in player.current_room.inventory.keys():
            player.inventory[list_of_words[1]]= player.current_room.inventory[list_of_words[1]]
            del player.current_room.inventory[list_of_words[1]]
            print()
            print("tu viens de prendre {}".format(list_of_words[1]))
            print()
        else:
            print("cet item n'est pas disponible")
        return True
   
    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        player=game.player
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        if list_of_words[1] in player.inventory.keys():
            player.current_room.inventory[list_of_words[1]]= player.inventory[list_of_words[1]]
            del player.inventory[list_of_words[1]]
            print()
            print("tu viens de deposer {}".format(list_of_words[1]))
            print()
        else:
            print("cet item n'est pas dans ton inventaire")
        return True

   
        """item_choisi = list_of_words[1]
        for i in game.player.inventory:
            if i.name == item_choisi :
                game.player.current_room.inventory.add(i)
                del game.player.inventory[i]
                print("\nCette item a été retiré à votre inventaire !")
            else:
                print("cet item n'est pas dans ton inventaire")    
            return True"""
        


        
#    """ def drop(game, list_of_words, number_of_parameters):
#         l = len(list_of_words)
#         if l != number_of_parameters + 1:
#             command_word = list_of_words[0]
#             print(MSG1.format(command_word=command_word))
#             return False
    
#         item_choisi = list_of_words[1]
#         for i in game.player.inventory:
#             if i.name == item_choisi : 
#                 game.player.current_room.inventory_room.add(i)
#                 del game.player.inventory[i]
#                 print("\nCette item a été retiré à votre inventaire !")
#                 return True

#         print("Cette item n'existe pas")"""

    def talk(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de parler à un personnage non joueur (PNJ) dans la pièce actuelle.

        Paramètres:
        -----------
        game : Game
            L'instance du jeu.
        arguments : list
            Les arguments passés avec la commande (par ex. ["talk", "gandalf"]).
        number_of_parameters : int
            Le nombre de paramètres requis par la commande.
        """
        
        """if len(list_of_words) - 1 < number_of_parameters:
            print("Cette commande nécessite un paramètre supplémentaire (le nom du personnage).")
            return

        # Récupérer le nom du personnage (2ème mot de la commande)
        character_name = list_of_words[1].lower()

        # Vérifier si le personnage existe dans la pièce actuelle
        current_room = game.player.current_room
        if character_name in current_room.characters:
            character = current_room.characters[character_name]
            character.get_msg()  # Appeler la méthode get_msg du PNJ
            
        
        else : 
            # Si aucun personnage n'a été trouvé
            print(f"\nIl n'y a aucun personnage nommé '{character_name}' ici.\n")"""

        #permet au joueur de connaître ce que les pnj ont a dire
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        player=game.player
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        print(game.player.current_room.inventory[list_of_words[1]])
        if list_of_words[1] in game.player.current_room.inventory.keys() :
                game.player.current_room.inventory[list_of_words[1]].get_msg()
        else:
                print(list_of_words[1] + " n'est pas disponible")
        return True
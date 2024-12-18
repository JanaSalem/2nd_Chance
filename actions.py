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
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True

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
        # Vérifiez si l'historique n'est pas vide
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
            return False
        
    def check(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
    
        game.player.print_inventory()
        return True

    def look(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:      #le joueur n'a pas correctement saisi la commande.
            command_word = list_of_words[0]
            print(MSG0.format(command_word = command_word))
            return False
   
        game.player.current_room.print_inventory_room()
        return True
    
    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
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
        print(f"\nVous avez pris l'objet '{item_name}'.")
        
   
    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
   
        item_choisi = list_of_words[1]
        for i in game.player.inventory:
            if i.name == item_choisi :
                game.player.current_room.inventory_room.add(i)
                del game.player.inventory[i]
                print("\nCette item a été retiré à votre inventaire !")
                return True


        print("Cette item n'existe pas")

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
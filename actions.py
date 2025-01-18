"""
Fichier actions.py

Ce fichier définit la classe Actions et ses méthodes associées, qui représentent les actions possibles dans le jeu d'aventure.
Ces actions permettent au joueur d'interagir avec des objets, des personnages, et de naviguer dans le monde du jeu.

Les principales méthodes incluent :
- `help`: Affiche les commandes disponibles au joueur.
- `quit`: Termine le jeu.
- `go`: Gère le déplacement du joueur entre les différentes pièces.
- `drop`: Permet au joueur de déposer des objets dans une pièce.
- `take`: Permet au joueur de ramasser des objets disponibles dans une pièce.
- `check`: Affiche l'inventaire du joueur.
-"Talk": Pour parler aux personnages.
Chaque méthode prend en compte des arguments spécifiques pour gérer les interactions appropriées avec les objets, les commandes et l'état du jeu.

Ce fichier est essentiel pour la logique des actions que le joueur peut effectuer tout au long de son aventure.
"""
import os
from PIL import Image
# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:
    """
    Classe représentant les actions possibles dans le jeu d'aventure.

    Cette classe contient une collection de méthodes qui permettent de gérer les actions que le joueur peut effectuer dans le jeu.
    Chaque méthode correspond à une action spécifique comme interagir avec des objets, dialoguer avec des personnages, ou naviguer dans le monde du jeu.

    Les méthodes incluent des actions telles que :
    - `help`: Affiche les commandes disponibles au joueur.
    - `quit`: Termine le jeu.
    - `go`: Gère le déplacement du joueur d'une pièce à une autre.
    - `back`: Retourne à la dernière pièce visitée.
    - `look`: Permet de voir les objets et les personnages présents dans la pièce.
    - `drop`: Permet au joueur de déposer un objet de son inventaire dans la pièce.
    - `take`: Permet au joueur de ramasser un objet disponible dans la pièce.
    -'talk': Permet de parler aux personnages
    Ces méthodes sont associées à des commandes spécifiques saisies par le joueur.

    Exemple d'utilisation des méthodes :
    - `Actions.help(game, list_of_words, number_of_parameters)`: Affiche l'aide au joueur.
    - `Actions.take(game, list_of_words, number_of_parameters)`: Gère la prise d'un objet de la pièce.
    - `Actions.check(game, list_of_words, number_of_parameters)`: Affiche l'inventaire du joueur.

    Note :
    - Certaines méthodes peuvent nécessiter des arguments supplémentaires comme la liste des mots d'une commande ou le nombre de paramètres attendus.
    """

    @staticmethod #NOUVEAUJ
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
        """

        player = game.player
        l = len(list_of_words)

        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words and convert to uppercase
        direction = list_of_words[1].upper()  # Convertir en majuscules

        # Vérifier si la direction est dans les alias et la convertir si nécessaire
        if direction in game.direction_aliases:
            direction = game.direction_aliases[direction]

        if direction in player.current_room.exits:
            # Move the player in the direction specified by the parameter.
            player.move(direction)
            player.current_room.visited = True
            # Afficher la description de la pièce actuelle
            print(player.current_room.get_long_description())
            if not player.current_room.visited:
                player.current_room.show_image()
        else:
            print("Direction non valide veuillez réessayer")

        return True


    def quit(self,game, list_of_words, number_of_parameters):
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

    def back(self,game, list_of_words, number_of_parameters):
        """
        Permet au joueur de revenir à la dernière pièce visitée.
        """
        player = game.player
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


    def check(self,game, list_of_words, number_of_parameters):
        """
        Permet au joueur de vérifier son inventaire.

        Args:
            game (Game): L'état du jeu.
            list_of_words (list): Commande contenant les détails à afficher.
            number_of_parameters (int): Nombre de paramètres attendus.

        Returns:
            bool: `True` si l'action est réussie, `False` sinon.

        Affiche les objets présents dans l'inventaire du joueur.

        Exemple :
        >>> check(game, ['check'], 0)
        """
        l = len(list_of_words)
        player=game.player
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        game.player.print_inventory()
        return True

    def look(self,game, list_of_words, number_of_parameters):
        """
        Permet au joueur de voir les objets et PNJ présents dans la pièce.

        Args:
            game (Game): L'état du jeu.
            list_of_words (list): Commande contenant les détails à afficher.
            number_of_parameters (int): Nombre de paramètres attendus.

        Returns:
            bool: `True` si l'action est réussie, `False` sinon.

        Affiche les objets et les personnages disponibles dans la pièce du joueur.

        Exemple :
        >>> look(game, ['look'], 0)
        """
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

    def take(self,game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un objet de la pièce actuelle.

        Args:
            game (Game): L'état du jeu.
            list_of_words (list): Commande contenant l'objet à prendre.
            number_of_parameters (int): Nombre de paramètres attendus.

        Returns:
            bool: `True` si l'objet est pris, `False` sinon.

        Si l'objet a une quête associée, le joueur doit réussir la quête pour le prendre.
        Sinon, l'objet est directement ajouté à l'inventaire du joueur.

        Exemple :
        >>> take(game, ['take', 'épée'], 1)
        """
        l = len(list_of_words)
        player = game.player

        # Vérification du nombre de paramètres
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]

        if item_name in player.current_room.inventory.keys():
            # Vérifier si l'objet a une quête associée
            if item_name in game.quetes:
                quest = game.quetes[item_name]
                if quest.ask_question():
                    # Ajouter l'objet à l'inventaire seulement si la quête est réussie
                    player.inventory[item_name] = player.current_room.inventory[item_name]
                    del player.current_room.inventory[item_name]
                    print(f"\ntu viens de prendre {item_name}")
                else:
                    game.finished = True  # Terminer le jeu si la quête échoue
                    return False
            else:
                # Si pas de quête, ajouter directement l'objet
                player.inventory[item_name] = player.current_room.inventory[item_name]
                del player.current_room.inventory[item_name]
                print(f"\ntu viens de prendre {item_name}")
        else:
            print("cet item n'est pas disponible")

        return True

    def drop(self,game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un objet dans la pièce actuelle.

        Args:
            game (Game): L'état du jeu.
            list_of_words (list): Commande contenant l'objet à déposer.
            number_of_parameters (int): Nombre de paramètres attendus.

        Returns:
            bool: `True` si l'objet est déposé, `False` sinon.

        Effectue le dépôt de l'objet dans la pièce et le retire de l'inventaire du joueur.

        Exemple :
        >>> drop(game, ['drop', 'épée'], 1)
        """
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

    def talk(self,game, list_of_words, number_of_parameters):
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

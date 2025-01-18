"""
Fichier actions.py

Ce fichier définit la classe Actions et ses méthodes associées pour le jeu d'aventure.
Il gère les interactions comme le déplacement, la manipulation d'objets et les dialogues.
"""

# Messages d'erreur pour les commandes
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """
    Classe gérant les actions possibles dans le jeu d'aventure.

    Cette classe implémente toutes les commandes disponibles pour le joueur comme:
    - help: Affiche l'aide
    - quit: Termine le jeu
    - go: Déplacement
    - take/drop: Gestion d'inventaire
    - talk: Dialogues avec PNJ
    """

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Déplace le joueur dans la direction spécifiée.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1].upper()
        player = game.player

        if direction in game.direction_aliases:
            direction = game.direction_aliases[direction]

        if direction in player.current_room.exits:
            player.move(direction)
            player.current_room.visited = True
            print(player.current_room.get_long_description())
            if not player.current_room.visited:
                player.current_room.show_image()
            return True

        print("Direction non valide veuillez réessayer")
        return False

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Termine le jeu.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande 
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Affiche l'aide du jeu.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print(f"\t- {command}")
        print()
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Retourne à la pièce précédente.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        if not player.history:
            print("Vous êtes à la case de départ")
            return False

        room = player.history.pop()
        player.current_room = room
        player.get_history()
        print(player.current_room.get_long_description())
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        game.player.print_inventory()
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Examine la pièce courante.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        game.player.current_room.print_inventory()
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Prend un objet dans la pièce.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player

        if item_name not in player.current_room.inventory:
            print("Cet item n'est pas disponible")
            return False

        if item_name in game.quetes:
            quest = game.quetes[item_name]
            if not quest.ask_question():
                game.finished = True
                return False

        player.inventory[item_name] = player.current_room.inventory[item_name]
        del player.current_room.inventory[item_name]
        print(f"\nVous avez pris {item_name}")
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Dépose un objet dans la pièce.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player

        if item_name not in player.inventory:
            print("Cet item n'est pas dans votre inventaire")
            return False

        player.current_room.inventory[item_name] = player.inventory[item_name]
        del player.inventory[item_name]
        print(f"\nVous avez déposé {item_name}")
        return True

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        Parle à un PNJ dans la pièce.

        Args:
            game: Instance du jeu
            list_of_words: Liste des mots de la commande
            number_of_parameters: Nombre de paramètres attendus

        Returns:
            bool: True si succès, False sinon
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        character_name = list_of_words[1].lower()

        if character_name not in game.player.current_room.inventory:
            print(f"{list_of_words[1]} n'est pas disponible dans cette pièce")
            return False

        character = game.player.current_room.inventory[character_name]
        character.get_msg()
        return True

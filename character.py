"""Module définissant les personnages non-joueurs du jeu d'aventure.

Ce module contient la classe Character qui gère les personnages non-joueurs (PNJ),
leurs caractéristiques et leurs comportements dans le jeu.
"""

class Character():
    """Classe représentant un personnage non-joueur (PNJ) dans le jeu.
    
    Cette classe définit les attributs et comportements des PNJ, incluant
    leur nom, description, localisation et dialogues.

    Attributes:
        name (str): Le nom du personnage.
        description (str): Une description du personnage.
        current_room: La pièce où se trouve actuellement le personnage.
        msg (list): Liste des messages/dialogues du personnage.
    """

    def __init__(self, name:str, description:str, current_room, msg:list):
        """Initialise un nouveau personnage.

        Args:
            name (str): Le nom du personnage.
            description (str): La description du personnage.
            current_room: La pièce de départ du personnage.
            msg (list): Liste des messages/dialogues du personnage.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msg = msg
        self.msg_index = 0  # 🌟 Indice pour suivre le message affiché

    def __str__(self):
        """Renvoie une représentation textuelle du personnage.

        Returns:
            str: Le nom et la description du personnage.
        """
        return str(self.name) + " : " +  str(self.description)

    def get_msg(self): #🌟
        """Affiche cycliquement les messages du personnage.

        Affiche le premier message de la liste puis le déplace à la fin,
        créant ainsi une rotation cyclique des messages.
        """
        if len(self.msg)<=0:
            return None
        else :
            msg=self.msg.pop(0)
            print(msg)
            self.msg.append(msg)

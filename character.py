import random
from random import randint
#from config import DEBUG
class Character():

    def __init__(self, name:str, description:str, current_room, msg:list):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msg = msg
        self.msg_index = 0  # 🌟 Indice pour suivre le message affiché
        
    def __str__(self):
        return str(self.name) + " : " +  str(self.description)
    

    """def move(self):
       
        Déplace le personnage non joueur dans une pièce adjacente avec une probabilité de 50% (1 chance sur 2).
        Retourne True si le personnage se déplace, False sinon.
        """
    """# Chance de 50% de se déplacer
        if random.choice([True, False]):
            # Vérifier qu'il y a des sorties disponibles
            if not self.current_room.exits:
                print(f"{self.name} ne peut pas se déplacer (pas de pièce adjacente).")
                return False
            
            # Choisir une pièce adjacente au hasard
            next_room = random.choice(list(self.current_room.exits.values()))

            # Déplacer le personnage vers la nouvelle pièce
            self.current_room.characters.remove(self)  # Retirer le personnage de la pièce actuelle
            if next_room.characters is None:  # Si la pièce n'a pas de personnages
                next_room.characters = {self}
            else:
                next_room.characters.add(self)  # Ajouter le personnage à la nouvelle pièce

            # Mettre à jour la pièce actuelle du personnage
            self.current_room = next_room

            # Afficher un message de débogage si DEBUG est activé
            if DEBUG:
                print(f"{self.name} se déplace vers {next_room.name}.")
            
            return True
        else:
            # Si le personnage reste dans la même pièce
            if DEBUG:
                print(f"{self.name} reste dans la même pièce.")
            return False"""
    """print(f"{self.name} tente de se déplacer...")
    
        # Afficher la pièce actuelle avant le déplacement
        print(f"{self.name} est actuellement dans la pièce: {self.current_room.name}")
        if random.choice([True, False]):
            # Vérifie s'il y a des sorties disponibles
            if not self.current_room.exits:
                print(f"{self.name} ne peut pas se déplacer (pas de pièces adjacentes).")
                return False
            
            # Choisir une pièce adjacente au hasard
            next_room = random.choice(list(self.current_room.exits.values()))
            
            # Déplacer le personnage dans la nouvelle pièce
            self.current_room.characters.remove(self)  # Retirer le personnage de la pièce actuelle
            if next_room.characters is None:  # Si la nouvelle pièce est vide
                next_room.characters = {self}
            else:
                next_room.characters.add(self)  # Ajouter à la nouvelle pièce

            # Mettre à jour la pièce actuelle du personnage
            self.current_room = next_room

            # Afficher les personnages présents dans la nouvelle pièce après déplacement
            print(f"Personnages dans {next_room.name} après le déplacement: {[character.name for character in next_room.characters]}")

            #Afficher la nouvelle pièce du personnage
            print(f"{self.name} est maintenant dans la pièce: {self.current_room.name}")
            return True
        else:
            # Si le personnage reste dans la même pièce
            print(f"{self.name} reste dans la même pièce.")
            return False  # Le personnage ne s'est pas déplacé"""

    """
        # Vérifie s'il y a des sorties dans la pièce actuelle
            if not self.current_room or not self.current_room.exits: # type: ignore
                print(f"{self.name} ne peut pas se déplacer, aucune sortie disponible.") # type: ignore
            
        
            # Une chance sur deux de se déplacer (50% de chance)
            if random.choice([True, False]):
                # Choisir une direction au hasard parmi les sorties disponibles
                next_room = random.choice(list(self.current_room.exits.values())) # type: ignore
                print(f"{self.name} se déplace vers {next_room.name}.") # type: ignore
            
            # Trouver la pièce adjacente à cette direction
            #next_room = self.current_room.exits[direction]
            
            # Déplacer le personnage dans la nouvelle pièce
            #del self.current_room.character(self.name)
            #self.current_room.characters.remove(self.name)  # Retire le personnage de la pièce actuelle
            #next_room.characters.add(self)  # Ajoute le personnage dans la nouvelle pièce
            

            #self.current_room = next_room  # Met à jour la pièce actuelle du personnage
            
            #print(f"{self.name} se déplace vers {next_room.name}.")
            #return True
            # Retirer de la pièce actuelle (utilise le nom comme clé)
                print(self.current_room.characters)
                self.current_room.characters.pop(self.name.lower())
                print(self.current_room.characters)
            
                # Mettre à jour la pièce actuelle
                self.current_room = next_room
            
                # Ajouter le personnage à la nouvelle pièce
                next_room.characters[self.name.lower()] = self
            """
            
            
        
    """else:
        # Le personnage reste dans la pièce actuelle
        print(f"{self.name} reste dans la pièce {self.current_room.name}.")
        return False"""



    def get_msg(self): #🌟
        """
        Affiche cycliquement les messages associés au personnage.

        Lorsqu'un message est affiché, il ne sera plus affiché dans les appels suivants,
        mais les messages sont réutilisés lorsque tous ont été affichés une fois.
        """
        if not self.msg:
            print(f"{self.name} n'a rien à dire.")
            return

        # Afficher le message correspondant à l'index actuel
        print(self.msg[self.msg_index])

        # Incrémenter l'index, et revenir à 0 lorsqu'on atteint la fin
        self.msg_index = (self.msg_index + 1) % len(self.msg)
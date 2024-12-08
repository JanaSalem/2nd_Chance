# Description: Game class


# Import modules


from room import Room
from player import Player
from command import Command
from actions import Actions


class Game:
    """
    Classe représentant le jeu d'aventure.


    Cette classe gère la configuration du jeu, les interactions entre le joueur, les pièces,
    et les commandes, ainsi que la boucle principale de jeu.


    Attributs:
    ----------
    finished : bool
        Indique si le jeu est terminé.
    rooms : list[Room]
        Liste des pièces disponibles dans le jeu.
    commands : dict[str, Command]
        Dictionnaire associant des mots-clés à des commandes.
    player : Player
        L'objet représentant le joueur.


    Méthodes:
    ---------
    __init__():
        Initialise les attributs de base du jeu.
    setup():
        Configure les pièces, les commandes, et initialise le joueur.
    play():
        Lance le jeu et gère la boucle principale.
    process_command(command_string: str) -> None:
        Traite une commande entrée par le joueur.
    print_welcome():
        Affiche un message de bienvenue au début du jeu.


    Exceptions:
    -----------
    Cette classe ne lève aucune exception directement,
    mais peut appeler des méthodes externes qui en lèvent.


    Exemples d’utilisation:
    -----------------------
    >>> game = Game()
    >>> game.setup()
    >>> game.print_welcome()
    Bienvenue [Nom du joueur] dans ce jeu d'aventure !
    Entrez 'help' si vous avez besoin d'aide.
    Vous êtes dans un marécage sombre et ténébreux. L'eau bouillonne, les abords sont vaseux.


    >>> game.process_command("help")
    [Affiche la liste des commandes disponibles]
    """


    def __init__(self):
        """
        Initialise les attributs de base pour un nouvel objet Game.
        """
        
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.valid_direction = set() # Initialise valid_direction comme un ensemble vide
        #Ajout le dictionnaire des alias et des directions 
        self.direction_aliases = {
            "N": "N", "NORD": "N",
            "E": "E", "EST": "E",
            "S": "S", "SUD": "S",
            "O": "O", "OUEST": "O",
            "NE": "NE", "NORD-EST": "NE",
            "NO": "NO", "NORD-OUEST": "NO",
            "SE": "SE", "SUD-EST": "SE",
            "SO": "SO", "SUD-OUEST": "SO"
        }
        
       


       

   
    def setup(self):
        """
        Configure les composants du jeu, y compris les pièces,
        les sorties, les commandes, et le joueur.
        """
        # Configuration des commandes (inchangé)
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O,NO,NE)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back"," Permet de revenir en arrière.", Actions.back, 0)  #🌸 
        self.commands["back"] = back 
         # Initialisez l'historique du joueur
        self.history = []



        # Configuration des pièces
        salon = Room("Salon", "au salon,un espace chaleureux et lumineux au cœur de la maison, entouré de baies vitrées donnant sur la nature luxuriante .")
        cave = Room("Cave", "dans la cave, un endroit sombre et frais où se trouvent des objets anciens et des armes de toutes sortes.")
        bureau = Room("Bureau", "au bureau, un lieu tranquille, entouré de Led de toutes les couleurs eclairant seules la pieces au centre plusieurs pc gamers pour un setup des plus immersifs.")
        salle_musique = Room("Salle de Musique", "dans une salle remplie d'instruments ,d'un piano qui résonne harmonieusement et d'un micro demandant d'acceuillir les plus belles voix.")
        jardin = Room("Jardin", "au jardin, un espace verdoyant où les plantes tropicales prospèrent.")
        veranda = Room("Véranda", "dans un endroit ouvert sur l'île, offrant une vue paisible sur la jungle et la plage qui est rempli d'intruments scientifiques des plus étranges.")
        chambre = Room("Chambre", "dans un refuge confortable avec un lit balladaquin ayant une vue maginifique sur le jardin.")
        dressing = Room("Dressing", "dans un endroit rempli de vêtements et d'accessoires de luxe, soigneusement organisés.")
        jungle = Room("Jungle", "dans un lieu dense et mystérieux rempli de faune exotique et mystique.")
        plage = Room("Plage", "dans un endroit idyllique, où le sable chaud rencontre la mer turquoise.")
        villa = Room("Villa", "dans la Villa, le point central de vie sur l'île, accueillant et protégé.")


        # Ajouter les pièces à la liste des pièces
        self.rooms = [salon, cave, bureau, salle_musique, jardin, veranda, chambre, dressing, jungle, plage, villa]


        # Configuration des sorties
        salon.exits = {"D": cave, "E": bureau, "S": salle_musique, "O": jardin, "NE": veranda, "U": chambre}
        cave.exits = {"S": salon, "O": jardin, "N": salon, "U": jardin}
        bureau.exits = {"O": salon, "E": salle_musique}
        salle_musique.exits = {"N": salon, "E": bureau, "U": chambre, "O": jardin}
        jardin.exits = {"N": salon, "D": cave, "E": veranda, "O": jungle, "U": dressing}
        veranda.exits = {"N": jungle, "S": jardin}
        chambre.exits = {"N": salle_musique, "E": dressing,"D": salon}  # Chambre monte vers le salon
        dressing.exits = {"O": chambre, "S": jardin, "D": jardin}
        jungle.exits = {"S": jardin, "N": veranda, "E": plage,"O":villa}
        plage.exits = {"O": jungle, "N": villa}
        villa.exits = {"S": plage,"O":jungle}


        # Configuration du joueur , setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = plage  # La plage est la pièce de départ


    def update_valid_direction(self):
        #met à jour les directions valides selon la pièce où est le joueur
        self.valid_direction = set(self.player.current_room.exits.keys())

       
    def play(self):
        """
        Démarre le jeu, affiche le message de bienvenue et lance la boucle principale.
        """
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))


    def process_command(self, command_string: str) -> None:
        """
        Analyse et exécute une commande entrée par le joueur.


        Paramètres:
        -----------
        command_string : str
            La commande entrée par le joueur, sous forme de chaîne de caractères.
        """
        # Supprime les espaces au début et à la fin de la chaîne de commande
        command_string = command_string.strip().lower()


        # Si la commande est vide, ne rien faire et retourner immédiatement
        if not command_string:
            return
        # Sépare la chaîne de commande en une liste de mots (par exemple "go N" devient ["go", "N"])
        list_of_words = command_string.split(" ")
        # Récupère le premier mot, qui est le mot de commande (par exemple "go")
        command_word = list_of_words[0]

        #Met la direction sous le bon format si besoin
        if len(list_of_words) > 1: #Condition permets de vérifier si le joueur a bien entré un deuxième mot après la commande(premier mot go et le deuxième N,..)
            
            raw_direction = list_of_words[1].upper()  # Convertir en majuscules, et les stockes
            if raw_direction in self.direction_aliases: # un dictionnaire où les clés sont les alias des directions
                list_of_words[1] = self.direction_aliases[raw_direction]  # Mapper vers la direction standard
            else:
                print(f"\n'{list_of_words[1]}' n'est pas une direction valide.")
                return



        # Si le mot de commande n'est pas reconnu, afficher un message d'erreur
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # Si le mot de commande est reconnu, exécuter l'action associée
        else:
            # Récupère l'objet Commande associé au mot de commande
            command = self.commands[command_word]
            # Appelle l'action associée à la commande, en passant le jeu, la liste des mots et le nombre de paramètres
            command.action(self, list_of_words, command.number_of_parameters)




    def print_welcome(self):
        """
        Affiche un message de bienvenue, incluant le nom du joueur
        et la description de la pièce initiale.
        """
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())




def main():
    # Create a game object and play the game
    Game().play()
   


if __name__ == "__main__":
    main()


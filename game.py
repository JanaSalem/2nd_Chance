# Description: Game class
# Import modules




from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item


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
        #self.direction_ensemble = set()
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
        look = Command("look","Permet de voir les objets de la pièce.", Actions.look, 0)#🌸 
        self.commands["look"] = look
        drop = Command("drop","Permet de déposer un objet dans l'inventaire,Action.drop",Actions.drop,0)
        self.commands["drop"] = drop
        take = Command("take","Permet de prendre un objet",Actions.take,1)
        self.commands["take"]= take
        drop = Command("drop","permet de reposer un objet",Actions.drop,1)
        self.commands["drop"]= drop
        check = Command("check","Permet de voir ce qui ce trouve dans son inventaire",Actions.check,0)
        self.commands["check"]= check


        """self.direction_ensemble.add("N")
        self.direction_ensemble.add("S")
        self.direction_ensemble.add("O")
        self.direction_ensemble.add("E")
        self.direction_ensemble.add("U")
        self.direction_ensemble.add("D")"""


        # Configuration des pièces
        salon = Room("Salon", "le salon,un espace chaleureux et lumineux au cœur de la maison, entouré de baies vitrées donnant sur la nature luxuriante .")
        cave = Room("Cave", " la cave, un endroit sombre et frais où se trouvent des objets anciens et des armes de toutes sortes.")
        bureau = Room("Bureau", "le bureau, un lieu tranquille, entouré de Led de toutes les couleurs eclairant seules la pieces au centre plusieurs pc gamers pour un setup des plus immersifs.")
        salle_musique = Room("Salle de Musique", "une salle remplie d'instruments ,d'un piano qui résonne harmonieusement et d'un micro demandant d'acceuillir les plus belles voix.")
        jardin = Room("Jardin", "un jardin, un espace verdoyant où les plantes tropicales prospèrent.")
        veranda = Room("Véranda", "un endroit ouvert sur l'île, offrant une vue paisible sur la jungle et la plage qui est rempli d'intruments scientifiques des plus étranges.")
        chambre = Room("Chambre", "un refuge confortable avec un lit balladaquin ayant une vue maginifique sur le jardin.")
        dressing = Room("Dressing", "un endroit rempli de vêtements et d'accessoires de luxe, soigneusement organisés.")
        jungle = Room("Jungle", "un lieu dense et mystérieux rempli de faune exotique et mystique.")
        plage = Room("Plage", "un endroit idyllique, où le sable chaud rencontre la mer turquoise.")
        villa = Room("Villa", "la Villa, le point central de vie sur l'île, accueillant et protégé.")


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
        villa.exits = {"S": plage,"O":jungle,"N": salon}



    

        #Ajout des objets
        bougie = Item("bougie", "une bougie parfumée", 0.2)
        lettre = Item("lettre", "une lettre d'amour qui semble inachevé", 0.1)
        receuil_de_poeme = Item("receuil de poèmes", "un livre ouvert et marqué par le temps qui semble avoir beaucoup servit est sur la table de chevet",0.5)
        robe_paillette = Item("robe pailletté", "une robe pailleté rose bonbon est préparé sur un mannequin", 0.7)
        maquillage = Item("maquillage", "plusieurs trousses remplis de maquillage sont mis a disposition sur l'ilot se situant au mileu du dressing", 0.5)
        fruits_enchantes= Item("fruits enchantés", "sur plusieurs arbres de la forêt tu peux apercevoir des fruits mystérieux qui semblent appétissant ils sont entouré de lumière, ils t'appellent", 4)
        partition = Item("partition", "tu trouves sur le piano une partition d'une mélodie qui te semblent mélodieuse", 1)
        micro = Item("micro", "un micro traine dans la pièce il semble attendre quelqu'un de particulier", 1)
        armes = Item("armes", "dans le fond de la pièce sur le mur tu vois une collection inéglable d'armes de toutes sortes et de toutes les tailles", 1)
        poignard = Item("poignard", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)
        épée = Item("épée", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)
        arc = Item("arc et fléches", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)
        revolver = Item("revolver", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)
        tablette = Item("tablette portable", "Dans cette sombre pièce tou vois branché à l'ordinateur une tablette mystérieuse", 1)
       
       
        salon.inventory_room ={bougie}
        cave.inventory_room ={armes,épée,poignard,revolver}
        bureau.inventory_room ={tablette}
        salle_musique.inventory_room ={partition,micro}
        chambre.inventory_room ={lettre,receuil_de_poeme}
        dressing.inventory_room ={robe_paillette,maquillage}
        jungle.inventory_room ={fruits_enchantes}
        


        #Inventaires par lieu :
        salon.inventory_room ={bougie}
        chambre.inventory_room ={lettre, receuil_de_poeme}
        dressing.inventory_room = {robe_paillette,maquillage}
        jungle.inventory_room ={fruits_enchantes}
        salle_musique.inventory_room ={partition,micro}
        cave.inventory_room = {armes,poignard,épée,arc,revolver}
        bureau.inventory_room= {tablette}




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
        # Sépare la chaîne de commande en une list* de mots (par exemple "go N" devient ["go", "N"])
        list_of_words = command_string.split(" ")
        # Récupère le premier mot, qui est le mot de commande (par exemple "go")
        command_word = list_of_words[0]

        if command_word == 'go':
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

        """# Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)"""


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

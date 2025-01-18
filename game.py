"""
Module Game

Ce module implémente le cœur du jeu d'aventure textuel.
Il définit la classe principale `Game`,
qui coordonne les interactions entre les différentes entités du jeu,
telles que les pièces,
les objets, les personnages, et le joueur.

Le module gère également la configuration initiale du jeu, la boucle principale, et
le traitement des commandes saisies par le joueur.

Classes:
--------
- Game : Classe principale représentant le jeu d'aventure.

Fonctionnalités principales:
----------------------------
- Configuration des pièces (Room), des objets (Item) et des personnages (Character).
- Gestion des déplacements entre les pièces et des interactions avec les objets.
- Prise en charge des commandes textuelles pour naviguer
 et interagir avec l'univers du jeu.
- Affichage des images associées aux pièces lors de leur première visite.
- Gestion des quêtes et des énigmes liées aux objets et aux personnages.
- Conditions de fin de jeu basées sur la progression du joueur.

Exemples d'utilisation:
-----------------------
1. Initialisation et démarrage du jeu :
    >>> from game import Game
    >>> game = Game()
    >>> game.play()

2. Interaction avec les commandes :
    - Saisissez "help" pour obtenir de l'aide.
    - Déplacez-vous avec "go [direction]" (ex : "go N").
    - Interagissez avec les objets et les personnages selon les commandes disponibles.
"""
# Import modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest

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
        #self.characters = {} #🌟
        #self.direction_ensemble = set()
        self.valid_direction = set() # Initialise valid_direction comme un ensemble vide
        self.quetes = {}
        #Ajout le dictionnaire des alias et des directions
        self.direction_aliases = {
            "N": "N", "NORD": "N",
            "E": "E", "EST": "E",
            "S": "S", "SUD": "S",
            "O": "O", "OUEST": "O",
            "NE": "NE", "NORD-EST": "NE",
            "NO": "NO", "NORD-OUEST": "NO",
            "SE": "SE", "SUD-EST": "SE",
            "SO": "SO", "SUD-OUEST": "SO",
            "U":"U","UP":"U","D":"D","DOWN":"D"

        }
        self.all_characters_talked = set()
        # Pour suivre les personnages avec qui on a parlé
        self.final_riddle_shown = False
        # Pour s'assurer que l'énigme finale n'est montrée qu'une fois

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
        go = Command("go",
        "<direction> : se déplacer dans une direction cardinale (N, E, S, O,NO,NE)",
        Actions.go,
        1)
        self.commands["go"] = go
        back = Command("back"," Permet de revenir en arrière.", Actions.back, 0)
        self.commands["back"] = back
         # Initialisez l'historique du joueur
        self.history = []
        look = Command("look"," Permet de voir les objets de la pièce.", Actions.look, 0)
        self.commands["look"] = look
        drop = Command("drop"," Permet de déposer un objet dans l'inventaire",Actions.drop,0)
        self.commands["drop"] = drop
        take = Command("take"," Permet de prendre un objet",
        Actions.take,1)
        self.commands["take"]= take
        drop = Command("drop"," permet de reposer un objet",Actions.drop,1)
        self.commands["drop"]= drop
        check = Command("check",
        " Permet de voir ce qui ce trouve dans son inventaire",Actions.check,0)
        self.commands["check"]= check
        talk = Command("talk"," Permet de parler au personnage sur l'île",Actions.talk,1)
        self.commands["talk"]= talk

        # Configuration des pièces
        salon = Room(
            "Salon",
            "le salon🛋️,un espace chaleureux et lumineux au cœur de la maison, entouré de baies vitrées"
            "donnant sur la nature luxuriante .",
            {}
        )
        cave = Room(
            "Cave",
            " la cave 🔦🦇,un endroit sombre "
            "et frais où se trouvent des objets anciens et des armes de toutes sortes.",
            {}
        )
        bureau = Room(
            "Bureau",
             "le bureau🧑🏻‍💻, un lieu tranquille, "
             "entouré de Led de toutes les couleurs eclairant seules la pieces"
             " au centre plusieurs pc gamers pour un setup des plus immersifs.",
             {}
        )
        jardin = Room(
            "Jardin",
             "un jardin, ˚˖𓍢ִ໋🍃✧˚.💚 un espace verdoyant"
             " où les plantes tropicales prospèrent.˚˖𓍢ִ໋🍃✧˚.💚⋆",
             {}
             )
        veranda = Room(
            "Véranda",
            "la véranda🧺🏚️🍂, un endroit ouvert sur l'île,"
            "offrant une vue paisible sur la jungle et la plage "
            "qui est rempli d'intruments scientifiques des plus étranges.",
            {}
         )
        chambre = Room(
            "Chambre",
             "la chambre🚪🛏️,un refuge confortable"
             " avec un lit balladaquin ayant une vue maginifique sur le jardin.",
             {}
        )
        dressing = Room(
            "Dressing", "👗👔un endroit rempli de vêtements "
            "et d'accessoires de luxe, soigneusement organisés.",
            {}
        )
        jungle = Room(
            "Jungle",
             "La Jungle,🏝️🦜🌊 🦍🐒un lieu dense et mystérieux"
             "rempli de faune exotique et mystique.",
             {}
        )
        plage = Room(
            "Plage",
             "La plage, 🌴🍹🍉⛱️🥥un endroit idyllique,"
             " où le sable chaud rencontre la mer turquoise.",
             {}
             )
        villa = Room(
            "Villa", "🏡la Villa, le point central de vie sur l'île,"
            "accueillant et protégé.",
            {}
        )
        salle_musique = Room(
            "Salle de Musique",
             "une salle remplie d'instruments 𝄞 ,d'un piano qui résonne harmonieusement"
             " et d'un micro demandant d'acceuillir les plus belles voix.",
             {}
        )

        # Ajouter les pièces à la liste des pièces
        self.rooms = [salon, cave, bureau, salle_musique, jardin, veranda, chambre, dressing, jungle, plage, villa]


        # Configuration des sorties
        salon.exits = {"D": cave, "E": bureau, "O": salle_musique,"U": chambre}
        cave.exits = {"U": salon}
        bureau.exits = {"O": salon, "E": jungle}
        salle_musique.exits = {"E": salon,"O": jardin}
        jardin.exits = {"E": salle_musique,"N": veranda, "S": jungle}
        veranda.exits = {"NE": jungle, "S": jardin}
        chambre.exits = {"O": dressing,"D": salon}  # Chambre monte vers le salon
        dressing.exits = {"E": chambre}
        jungle.exits = {"N0": veranda, "SO": plage, "N":jardin}
        plage.exits = {"E": jungle, "N": villa}
        villa.exits = {"S": plage,"E":jungle,"N": salon}

        #Ajout des objets pou un jeu plus long
        # #épée = Item("épée", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)
        # #maquillage = Item("maquillage", "plusieurs trousses remplis de maquillage sont mis a disposition sur l'ilot se situant au mileu du dressing", 0.5)
        # #fruits= Item("fruits enchantés", "sur plusieurs arbres de la forêt tu peux apercevoir des fruits mystérieux qui semblent appétissant ils sont entouré de lumière, ils t'appellent", 4)

        poisson = Item("poisson magique🐟","Un peu de chance, on ne dit pas non...",1)
        chocolat = Item("chocolat🍫","J'espère que tu n'es pas allergique à cette merveille",1)
        bougie = Item("bougie🕯️", "une bougie parfumée", 0.2)
        receuil = Item("receuil de poèmes📜🪶", "un livre ouvert et marqué par le temps qui semble avoir beaucoup servit est sur la table de chevet",0.5)
        tablette = Item("tablette portable📱", "Dans cette sombre pièce tu vois branché à l'ordinateur une tablette mystérieuse", 1)
        partition = Item("partition 🎻", "tu trouves sur le piano une partition d'une mélodie qui te semble mélodieuse", 1)
        chat = Item("chat bleu magique 🐈‍⬛","Voudras-tu de la compagnie dans ton aventure?",1)
        arc = Item("arc et fléches🏹", "Prendras-tu cette arme pour t'accompagner lors de ton aventure ?", 1)


        plage.inventory['poisson']=poisson
        villa.inventory['chocolat']=chocolat
        salon.inventory['bougie'] = bougie
        chambre.inventory['receuil']=receuil
        bureau.inventory['tablette']=tablette
        salle_musique.inventory['partition']=partition
        jardin.inventory['chat']= chat
        veranda.inventory['arc']= arc

        #si on veux un jeu plus long
        # cave.inventory['épée'] = épée
        # jardin.inventory['chat']= chat
        # veranda.inventory['arc']= arc
        # dressing.inventory['maquillage']=maquillage
        # jungle.inventory['fruits']=fruits


        # Setup Personnages
        beyonce = Character("Beyonce", "La star ⭐", salle_musique,
        ["\nJe suis une star tout le monde me connaît"
        " je suis reconnu partout où je vais,cette maison n'est pas à ma hauteur,\nM'observe pas comme ça tu devrais plutôt aller voir Orion.\nJ'ai entendu dire qu'il était devenu fou et avait inventé des sérums pour 'faire rajeunir les gens' mais qu'il les défigurait à la place pour que tout le monde lui ressemble .\nTu es surpris de ce que tu apprends,certes il est toujours enfermé dans la veranda comme-ci personne ne pouvait le voir"])
        jack = Character("Jack Letombeur","Le seducteur endiablé ❤️",chambre,
        ["Ravie d'avoir enfin la possibilité de te parler yeux dans les yeux mon/ma jolie."
        "\nPourquoi veux-tu t'éloigner de moi?, reste je sais ce que tu veux c'est bon je serais calme."
        "\nComme je suis si beau Beyonce s'est confié"
        " je sais qu'elle n'a pas hésiter à éliminer des gens sur son passage pour être la star qu'elle est"])
        lloyde = Character("Lloyde","Le gameur déchu🎮",bureau,
        ["\nFerme la porte je travailles.\nJe sais ce que tu veux "
        "si tu reviens plus jamais me voir je te le dis."
        "\nJ'ai fait mes recherches, Méfie de toi de Jack il a pour habitude de profiter de ses 'charmes'"
        "pour arnaquer les gens.\n Il va très loin et promets le grand amour puis"
        " les quitte en prenant l'argent et certains de désespoir amoureux sont morts. "])
        orion = Character("Orion","Le scientifique fou ⚛︎ 🧬 🧫 🧪",veranda,
        ["\nAHAHAH je t'attendais mon petit, tu es gênés de me voir defiguré ?"
        " C'est pas grave j'ai l'habitude.\nObserve un vrai laboratoire"
        " de VRAI science pas comme ce que fait ce hacker de Lloyde,"
        " tu sais qu'il travaillais dans la vente d'armes pour des terroristes sur le darkweb ?"
        " Mais bien sûr pour lui c'est normal même si des milliers de personnes meurent par sa faute."])

        salle_musique.inventory['beyonce'] = beyonce
        chambre.inventory['jack'] = jack
        bureau.inventory['lloyde'] = lloyde
        veranda.inventory['orion'] = orion

        # Setup player and starting room
        for room in self.rooms:
            for d in room.exits.keys():
                self.valid_direction.add(d)


#########################################################################################
                        # Configuration des quêtes 🎮
        quest1 = Quest("🕯️ Résolvez cette énigme pour activer la bougie:",
                    "Convertissez 10111001 en décimal.", "185")

        quest2 = Quest("📱 Trouvez le mot de passe pour la tablette.",
                    "Je suis un nombre à 4 chiffres:\nMon 1er chiffre est la moitié de mon 2nd,\nLa somme de tous mes chiffres est 18,\nMon 2nd est égal à mon 3ème.\nMon dernier est mon 1er.\nQui suis-je?", "3663")

        quest3 = Quest("🤔 Trouveras-tu cette énigme ?",
                    "Je vole sans ailes,\nje pleure sans yeux.\nQui suis-je ?", "un nuage")

        quest4 = Quest("🎵 Jouez la bonne mélodie.",
                    "Quelle note est entre Do et Mi ?", "Ré")

        #quest5 = Quest("🤔Trouveras-tu le bon animal ?",
                    #"Je suis un prédateur silencieux,\nje vole la nuit et j'ai des yeux perçants.\nQui suis-je ?", "Un hibou")

        #quest7 = Quest("💄 Apprenez l'art du maquillage.",
                    #"Résolvez : 54 × 584", "31536")

        #quest8 = Quest("👑 Hmm, question difficile :",
                    #"Quelle est l'emblème du Roi Soleil (Louis XIV) ?", "astre solaire")

        quest9 = Quest("🎓 La réponse est tellement logique :",
                    "Quelle est la meilleure classe prépa ?", "PSI")

        quest10 = Quest("🧩 Réfléchis un peu...",
                    "Girafe = 3,\nÉléphant = 3,\nHippopotame = 5,\nLion = … ?", "2")

        quest11 = Quest("💫 Une facile pour toi :",
                    "Qu'est-ce qui est plein de trous mais arrive quand même à retenir l'eau ?", "Une éponge")

        # Association des quêtes aux objets
        self.quetes = {
            'bougie': quest1,
            'tablette': quest2,
            'receuil': quest3,
            'partition': quest4,
            #'fruits': quest5,
            #'maquillage': quest7,
            #'épée': quest8,
            'chat': quest9,
            'arc': quest10,
            'poisson': quest11
        }

        # Configuration du joueur , setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = plage  # La plage est la pièce de départ


    def update_valid_direction(self):
        """
        met à jour les directions valides selon la pièce où est le joueur
        """
        self.valid_direction = set(self.player.current_room.exits.keys())

    def play(self): #NOUVEAU
        """
        Démarre le jeu et gère la boucle principale
        """
        self.setup()
        self.print_welcome()

        while not self.finished:
            if self.check_end_game_conditions() and not self.final_riddle_shown:
                self.show_final_riddle()
                if self.finished:  # Si l'énigme finale est résolue
                    break  # Sort de la boucle immédiatement

            # Attendre la commande de l'utilisateur sans réafficher la description
            self.process_command(input("> "))


    def check_end_game_conditions(self):
        """
        Vérifie si toutes les conditions de fin de jeu sont remplie
        s"""
        # Liste de tous les objets requis (excluant les personnages)
        required_items = {'bougie', 'tablette', 'receuil', 'partition',
                         'chat', 'arc', 'poisson', 'chocolat'}

        # Liste de tous les personnages
        all_characters = {'beyonce', 'jack', 'lloyde', 'orion'}

        # Vérifie si le joueur a tous les objets requis
        player_items = set(self.player.inventory.keys())
        has_all_items = required_items.issubset(player_items)

        # Vérifie si le joueur a parlé à tous les personnages
        talked_to_all = self.all_characters_talked == all_characters

        return has_all_items and talked_to_all


    def show_final_riddle(self):
        """
        Affiche l'énigme finale du jeu
        """
        if not self.final_riddle_shown:
            print("\n🌟 FÉLICITATIONS ! Vous avez découvert tous les secrets de l'île ! 🌟")
            print("\nUne dernière énigme vous attend...")
            print("\nÉnigme finale:")
            print("Je suis ce qui unit les âmes perdues,")
            print("Dans mes murs se cachent vérités et mensonges confondus.")
            print("Chaque habitant porte un masque différent,")
            print("Mais tous sont liés par un même tourment.")
            print("Qui suis-je?\n")

            reponse = input("Votre réponse: ").lower().strip()

            if reponse == "la villa":  # La réponse à l'énigme finale
                print("\n🎉 VICTOIRE ! 🎉")
                print("Vous avez percé le mystère de la villa et de ses habitants !")
                print("Chaque personnage a oublié son passé sombre. Vous êtes le seul qui a essayé de percer les mystères de l'île.")
                print("Les autres ont préféré rester dans le confort et ne pas chercher la vérité.")
                print("Sauf que ce que personne ne savait, c'est que cette île était leur seconde et dernière chance de vivre une belle vie pour pardonner leurs crimes.")

                while True:
                    print("\n⚠️ Une décision cruciale vous attend ⚠️")
                    print("\nVous avez deux choix :")
                    print("1. 🏝️ Rester sur l'île et oublier votre passé comme les autres")
                    print("2. 🚪 Partir et retourner à votre vie d'avant")

                    choix = input("\nVotre choix (1 ou 2): ").strip()

                    if choix == "1":
                        print("\n🌅 Vous choisissez de rester sur l'île...")
                        print("Vos souvenirs commencent doucement à s'effacer...")
                        print("Vous rejoignez les autres habitants dans leur paisible ignorance.")
                        print("\n🔚 FIN : Le Paradis Artificiel 🌴")
                        break
                    elif choix == "2":
                        print("\n🌊 Vous choisissez de partir...")
                        print("En quittant l'île, tous vos souvenirs reviennent.")
                        print("Vous vous rappelez de tout, y compris des raisons qui vous ont amené ici.")
                        print("Cette vérité sera votre fardeau à porter.")
                        print("\n🔚 FIN : Le Prix de la Vérité 🎭")
                        break
                    else:
                        print("\n❌ Choix invalide. Veuillez choisir 1 ou 2.")

                self.finished = True
            else:
                print("\n❌ Ce n'est pas la bonne réponse... Continuez d'explorer pour comprendre le mystère.")

            self.final_riddle_shown = True


    def process_command(self, command_string: str) -> None:
        """
        Analyse et exécute une commande entrée par le joueur
        """
        # Ne traite pas les commandes si le jeu est terminé
        if self.finished:
            return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word == "talk" and len(list_of_words) > 1:
            character_name = list_of_words[1].lower()
            self.all_characters_talked.add(character_name)

        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

        if command_word == 'go':
            if len(list_of_words) > 1:
                raw_valid_direction = list_of_words[1].upper()
                if raw_valid_direction in self.direction_aliases:
                    list_of_words[1] = self.direction_aliases[raw_valid_direction]
                else:
                    print(f"\n'{list_of_words[1]}' n'est pas une direction valide.")
                    return


    def print_welcome(self): # NOUVEAU
        """
        Affiche un message de bienvenue et la description initiale
        """
        print("""
        🌴 Vous ouvrez les yeux... Une plage inconnue, des vagues tranquilles, mais aucun souvenir de votre passé. Qui êtes-vous ? Pourquoi êtes-vous ici ? 🤔

        🎯 **Votre mission :** Résolvez les énigmes disséminées sur cette île mystérieuse pour découvrir la vérité sur ses secrets et ses habitants.

        🗣️ **Commandes utiles :**
        - **talk** : Parlez aux PNJ pour obtenir des indices précieux.
        - **go <direction>** : Déplacez-vous (Nord, Sud, Est, Ouest, Haut, Bas).

        🕵️‍♂️ Bonne chance, détective ! L'île garde ses secrets... saurez-vous les révéler ? 🌟
    """)

        print("Entrez 'help' si vous avez besoin d'aide.")
        print(f"Vous êtes dans {self.player.current_room.description}")
        print("Sorties:", ", ".join(self.player.current_room.exits.keys()))


def main():
    """
    Create a game object and play the game
    """
    Game().play()



if __name__ == "__main__":
    main()

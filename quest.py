"""
Module Quest

Ce module définit la classe `Quest`, qui représente une quête incluant une description,
une question, une réponse et un mécanisme de tentative pour répondre correctement.
"""
class Quest:
    """
    Classe représentant une quête avec une question et une réponse.

    Cette classe permet de gérer les quêtes du jeu en posant des questions au joueur.
    Le joueur a un nombre limité d'essais pour répondre correctement.

    Attributs:
    ----------
    description : str
        Une brève description de la quête.
    question : str
        La question posée au joueur pour cette quête.
    answer : str
        La réponse correcte à la question.
    attempts : int
        Le nombre maximum d'essais autorisés pour répondre à la question.

    Méthodes:
    ---------
    __init__(description, question, answer):
        Initialise une nouvelle quête avec une description, une question et une réponse.

    ask_question():
        Affiche la description et la question de la quête, 
        puis permet au joueur de tenter de répondre.
        Retourne True si le joueur répond correctement, 
        sinon False après épuisement des essais.

    Exemples d'utilisation:
    -----------------------
    >>> quest = Quest("Résolvez cette énigme:", "Quelle est la capitale de la France ?", "Paris")
    >>> quest.ask_question()
    Résolvez cette énigme:
    Question : Quelle est la capitale de la France ?
    Votre réponse : Lyon
    Incorrect ! Il vous reste 2 essais.
    Votre réponse : Paris
    Bravo ! Vous avez réussi !
    True
    """
    def __init__(self, description, question, answer):
        self.description = description
        self.question = question
        self.answer = answer
        self.attempts = 3  # Ajout de l'attribut attempts ici

    def ask_question(self):
        """
        Pose la question de la quête au joueur et gère ses réponses.

        Affiche la description de la quête, la question et permet au joueur d'y répondre. 
        Le joueur a un nombre limité d'essais pour répondre correctement.

        Returns:
            bool: True si le joueur répond correctement, False s'il épuise ses tentatives.
        """
        print(f"\n{self.description}")
        print(f"Question : {self.question}")
        while self.attempts > 0:
            user_answer = input("Votre réponse : ")
            if user_answer.lower() == self.answer.lower():
                print("Bravo ! Vous avez réussi !")
                return True
            else:
                self.attempts -= 1
                if self.attempts > 0:
                    print(f"Incorrect ! Il vous reste {self.attempts} essais.")
                else:
                    print("Game Over ! Vous avez épuisé tous vos essais.")
                    return False
        return False

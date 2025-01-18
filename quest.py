class Quest:
    def __init__(self, description, question, answer):
        self.description = description
        self.question = question
        self.answer = answer
        self.attempts = 3  # Ajout de l'attribut attempts ici

    def ask_question(self):
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
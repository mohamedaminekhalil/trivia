from question_generator import QuestionData
import random

# All categories possible to get with their id from the API docs
CATEGORIES_LIST = [("General knowledge", 9), ("Books", 10), ("Movies", 11), ("Music", 12), ("video games", 15),
                   ("science", 17), ("computer science", 18), ("Math", 19), ("Mythology", 20), ("sports", 21),
                   ("Geography", 22), ("History", 23), ("Art", 25), ("Celebs", 26), ("Animals", 27),
                   ("Anime & Manga", 31)]


# Setup class brain and initiate variables need it
class Brain:
    def __init__(self):
        self.money = 1_000_000
        self.stage = 1
        self.choices = 0
        self.current_question = None
        self.current_categories = None

    # Generate 2 randoms categories for user to pick one of them
    def generate_categories(self):
        self.current_categories = random.sample(CATEGORIES_LIST, k=2)

    # Generate question based on current stage and category picked
    def pick_question(self, cat):
        CATEGORIES_LIST.remove(cat)
        if self.stage <= 4:
            self.choices = 4
            stage = "easy"
        elif self.stage <= 7:
            self.choices = 3
            stage = "medium"
        else:
            self.choices = 2
            stage = "hard"
        self.current_question = QuestionData(cat[1], stage)

    # Calculate money left and return position of correct answer
    def after_math(self, bets):
        correct = 0
        for answer in range(0, self.choices):
            if self.current_question.choices[answer] != self.current_question.correct_answer:
                self.money -= bets[answer]
            else:
                correct = answer
        self.stage += 1
        return correct

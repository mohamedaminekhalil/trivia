from tkinter import *
from brain import Brain

FONT = ("Helvetica", 24, "bold")

brain = Brain()


class Images:
    def __init__(self):
        self.current_stage = PhotoImage(file="images/current_stage.png")
        self.stage_box = PhotoImage(file="images/stage_square.png")
        self.bg = PhotoImage(file="images/bg.png")
        self.money_img = PhotoImage(file="images/money.png")
        self.money1_img = PhotoImage(file="images/money1.png")
        self.category_img = PhotoImage(file="images/category.png")
        self.answers_screen_img = PhotoImage(file="images/screen.png")
        self.add_button_img = PhotoImage(file="images/+.png")
        self.minus_button_img = PhotoImage(file="images/-.png")
        self.money_on_img = PhotoImage(file="images/bet.png")
        self.wrong_img = PhotoImage(file="images/wrong.png")
        self.correct_img = PhotoImage(file="images/correct.png")
        self.lost_img = PhotoImage(file="images/bet_lost.png")
        self.kept_img = PhotoImage(file="images/bet_kept.png")
        self.drop_img = PhotoImage(file="images/drop.png")
        self.undrop_img = PhotoImage(file="images/undrop.png")


# Screen to show the current stage
class StageUi(Canvas):
    def __init__(self):
        super().__init__()
        self.images = Images()
        self.configure(width=1000, height=500, bg="blue", highlightthickness=0)
        self.pack(fill="both")
        self.stage = brain.stage
        self.money = brain.money
        self.create_image(500, 250, image=self.images.bg)
        self.create_text(250, 100, text="Questions :", fill="white", font=FONT)
        self.init()
        self.after(3000, self.next)

    def init(self):
        for x in range(0, 8):
            if x == self.stage - 1:
                self.create_image(250 + x * 75, 150, image=self.images.current_stage)
                self.create_text(250 + x * 75, 150, text=x + 1, fill="white", font=FONT)
            else:
                self.create_image(250 + x * 75, 150, image=self.images.stage_box)
                self.create_text(250 + x * 75, 150, text=x + 1, fill="white", font=FONT)
        self.create_image(500, 225, image=self.images.money_img)
        self.create_text(500, 225, text=f"${self.money}", fill="white", font=FONT)

    def next(self):
        self.destroy()
        brain.generate_categories()
        PickCategoryUi(brain.current_categories)


# Screen represents 2 categories user can pick from
class PickCategoryUi(Canvas):
    def __init__(self, category):
        super().__init__()
        self.images = Images()
        self.configure(width=1000, height=500, bg="blue", highlightthickness=0)
        self.pack(fill="both")
        self.create_image(500, 250, image=self.images.bg)
        self.create_text(300, 100, text="Pick a category...", fill="white", font=FONT)
        self.cat1 = self.create_image(325, 200, image=self.images.category_img)
        self.cat1_text = self.create_text(325, 200, text=category[0][0], font=(FONT[0], 16, FONT[2]), fill="white")
        self.cat2 = self.create_image(675, 200, image=self.images.category_img)
        self.cat2_text = self.create_text(675, 200, text=category[1][0], font=(FONT[0], 16, FONT[2]), fill="white")
        self.tag_bind(self.cat1, "<Button-1>", lambda event, cat=category[0]: self.next(event, cat))
        self.tag_bind(self.cat2, "<Button-1>", lambda event, cat=category[1]: self.next(event, cat))
        self.tag_bind(self.cat1_text, "<Button-1>", lambda event, cat=category[0]: self.next(event, cat))
        self.tag_bind(self.cat2_text, "<Button-1>", lambda event, cat=category[1]: self.next(event, cat))

    def next(self, event, cat):
        self.destroy()
        brain.pick_question(cat)
        QuestionUi(brain.stage, brain.money, brain.current_question)


# Screen of the question and answers and ability to place the money around the answers
class QuestionUi(Canvas):
    def __init__(self, stage, money, qdata):
        super().__init__()
        self.money = money
        self.lock = False
        self.num_choices = len(qdata.choices)
        self.images = Images()
        self.configure(width=1000, height=500, bg="blue", highlightthickness=0)
        self.pack(fill="both")
        self.create_image(500, 250, image=self.images.bg)
        self.create_image(170, 90, image=self.images.stage_box)
        self.create_text(170, 90, text=stage, fill="white", font=FONT)
        self.create_image(805, 75, image=self.images.money1_img)
        self.money_ui = self.create_text(805, 75, text=f"${self.money}", fill="white", font=(FONT[0], 12, FONT[2]))
        self.create_text(500, 150, text=qdata.question, fill="white", font=(FONT[0], 16, FONT[2]), justify="center")
        self.screens_bets = [0] * self.num_choices
        self.screens = []
        if stage <= 4:
            screens = 4
            x = 200
        elif stage <= 7:
            screens = 3
            x = 300
        else:
            screens = 2
            x = 400
        options = ['A.', 'B.', 'C.', 'D.']
        for screen in range(0, screens):
            screen_ = self.create_image(x + screen * 200, 300, image=self.images.answers_screen_img)
            bet = self.create_image(x + screen * 200, 400, image=self.images.money_on_img)
            add = self.create_image(x + screen * 200 + 60, 400, image=self.images.add_button_img)
            minus = self.create_image(x + screen * 200 - 60, 400, image=self.images.minus_button_img)
            bet_text = self.create_text(x + screen * 200, 400, text=f"${self.screens_bets[screen]}k", fill="white",
                                        font=(FONT[0], 15, FONT[2]))
            screen_ui = (screen_, bet, add, minus, bet_text)
            self.screens.append(screen_ui)
            self.create_text(x + screen * 200 - 60, 240, text=options[screen], fill="white",
                             font=(FONT[0], 12, FONT[2]))
            self.create_text(x + screen * 200, 300, text=qdata.choices[screen], fill="white",
                             font=(FONT[0], 12, FONT[2]), justify="center")
            self.tag_bind(self.screens[screen][2], "<Button-1>",
                          lambda event, index=screen: self.click_add(event, index))
            self.tag_bind(self.screens[screen][3], "<Button-1>",
                          lambda event, index=screen: self.click_minus(event, index))
        self.drop_button = self.create_image(500, 460, image=self.images.undrop_img)
        self.tag_bind(self.drop_button, "<Button-1>", lambda event: self.drop(event))

    def click_add(self, event, index):
        def add():
            self.screens_bets[index] += 25000
            if self.screens_bets[index] == 1000000:
                self.itemconfig(self.screens[index][4], text=f"${self.screens_bets[index] // 1000000}M")
            else:
                self.itemconfig(self.screens[index][4], text=f"${self.screens_bets[index] // 1000}k")

        if not self.lock:
            if sum(self.screens_bets) < self.money:
                if self.screens_bets.count(0) == 1:
                    if self.screens_bets[index] != 0:
                        add()
                else:
                    add()
        self.update_drop()

    def click_minus(self, event, index):
        if not self.lock:
            if self.screens_bets[index] != 0:
                self.screens_bets[index] -= 25000
                self.itemconfig(self.screens[index][4], text=f"${self.screens_bets[index] // 1000}k")
        self.update_drop()

    def update_drop(self):
        if sum(self.screens_bets) == brain.money:
            self.itemconfig(self.drop_button, image=self.images.drop_img)
        else:
            self.itemconfig(self.drop_button, image=self.images.undrop_img)

    def drop(self, event):
        if sum(self.screens_bets) == self.money:
            self.lock = True
            correct = brain.after_math(self.screens_bets)
            self.money = brain.money
            self.itemconfig(self.money_ui, text=f"${self.money}")
            for screen in range(0, self.num_choices):
                if screen != correct:
                    self.itemconfig(self.screens[screen][0], image=self.images.wrong_img)
                    self.itemconfig(self.screens[screen][1], image=self.images.lost_img)
                else:
                    self.itemconfig(self.screens[screen][0], image=self.images.correct_img)
                    self.itemconfig(self.screens[screen][1], image=self.images.kept_img)

        if brain.money > 0:
            if brain.stage <= 8:
                self.after(3000, self.next)
            else:
                self.after(3000, self.ending)
        else:
            self.after(3000, self.ending)

    def next(self):
        self.destroy()
        StageUi()

    def ending(self):
        self.destroy()
        ResultScreen()


# Result of how many money you won
class ResultScreen(Canvas):
    def __init__(self):
        super().__init__()
        self.images = Images()
        self.configure(width=1000, height=500, bg="blue", highlightthickness=0)
        self.pack(fill="both")
        self.money = brain.money
        self.create_image(500, 250, image=self.images.bg)
        self.create_text(500, 175, text=f"You walked out with ${self.money}", fill="white", font=FONT, justify="center")
        self.after(5000, self.quit)

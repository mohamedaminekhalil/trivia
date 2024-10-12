import requests
import random
import html

API_ENDPOINT = "https://opentdb.com/api.php"
TOKEN_API = "https://opentdb.com/api_token.php?command=request"


# Generate token to use with the api request
def generate_token():
    token_req = requests.get(url=TOKEN_API)
    new_token = token_req.json()["token"]
    return new_token


# Avoid text being off the answers card or question card
def cleanup(string, maxi):
    words = string.split()
    length = 0
    new_string = ""
    for word in words:
        length += len(word)
        if length > maxi:
            new_string += f"\n{word} "
            length = len(word) + 1
        else:
            new_string += f"{word} "
            length += 1
    return new_string


# Question class
class QuestionData:
    def __init__(self, category_id, stage):
        self.category = category_id
        self.token = generate_token()
        self.stage = stage
        self.question = ""
        self.choices = []
        self.correct_answer = ""
        self.generate_question()

    def generate_question(self):
        params = {
            "amount": 1,
            "category": self.category,
            "difficulty": self.stage,
            "type": "multiple",
            "token": self.token
        }
        req = requests.get(url=API_ENDPOINT, params=params)
        data = req.json()
        if data["response_code"] == 0:
            self.question = cleanup(data["results"][0]["question"], 25)
            self.question = html.unescape(self.question)
            self.correct_answer = html.unescape(cleanup(data["results"][0]["correct_answer"], 15))
            self.choices.append(self.correct_answer)
            if self.stage == "easy":
                n_c = 3
            elif self.stage == "medium":
                n_c = 2
            else:
                n_c = 1
            for answer in range(0, n_c):
                self.choices.append(html.unescape(cleanup(data["results"][0]["incorrect_answers"][answer], 15)))
            random.shuffle(self.choices)

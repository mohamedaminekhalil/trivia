# Trivia Game

A trivia game built with Tkinter that challenges players with multiple-choice questions and certain amount of money he need to manage. 
Players can strategically place money on answers, mirroring a 'Money Drop' style of gameplay.

## Features
- Multiple-choice questions sourced from [Open Trivia Database](https://opentdb.com/).
- Stage progression that affects question difficulty
  - 1-4 easy level 4 options.
  - 5-7 medium level 3 options.
  - 8 last and hard level 50/50 question.
- Category selection 2 category to pick from and every category been picked can't be picked again.
- Each option has two buttons to add or remove money placed on them.
- A 'Drop Money' button that reveals the correct answer, activated only when the total money placed equals the money left.

## Requirements
- Python 3.x
- Tkinter (included with standard Python installations)
- Requests (for API calls)
- An API token from [Open Trivia Database](https://opentdb.com/) (instructions below).

## API Token
To use the trivia game, you need an API token:
1. Go to [Open Trivia Database](https://opentdb.com/) and create an account if you don't have one.
2. Follow the instructions on their site to generate your API token.
3. Once you have your token, create a file named `config.py` in the project directory and add the following line:
```python
API_TOKEN = 'your_api_token_here'
Make sure to replace 'your_api_token_here' with your actual token.
```

How to Play

## How to Play
1. Start the game and select a category from the available options. Categories already chosen in previous rounds will be hidden.
2. Answer questions according to the current stage's difficulty.
3. Use the + and - buttons next to each answer to place or remove money on it.
4. When you're ready, press the 'Drop Money' button to reveal the correct answer. This button will only activate when the total money placed on the answers equals the money you have left.
5. If you lose all your money, you are out of the game.
6. If you answer the last question correctly you win the money you have left

## Usage Instructions
1. Clone the repository.
2. Install the required packages: 
```bash
pip install request
python main.py

## Acknowledgments
- Questions are provided by [Open Trivia Database](https://opentdb.com/).

from flask import Flask, render_template, request, redirect, url_for
import random
from art import logo

app = Flask(__name__)

# Global variables to keep track of the game state
user_cards = []
computer_cards = []

def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
   """Take a list of cards and return the score calculated from the cards"""
    #Check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in the game.
   if sum(cards) == 21 and len(cards) == 2:
        return 0
   #Check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. 
   if 11 in cards and sum(cards) > 21:
      cards.remove(11)
      cards.append(1)
   return sum(cards)
    # ... (your existing calculate_score code here)

def compare(user_score, computer_score):
   if user_score > 21 and computer_score > 21:
        return "BOTH WENT OVER! IT'S A DRAW!"

   if user_score == computer_score:
        return "IT'S A DRAW!"
   elif computer_score == 0:
      return "YOU LOSE, OPPONENT HAS BLACKJACK!"
   elif user_score == 0:
      return "YOU WIN WITH A BLACKJACK!"
   elif user_score > 21:
      return "YOU WENT OVER! YOU LOSE!"
   elif computer_score > 21:
      return "OPPONENT WENT OVER! YOU WIN!"
   elif user_score > computer_score:
      return "YOU WIN!"
   else:
      return "YOU LOSE!"
    # ... (your existing compare code here)

@app.route('/')
def start_game():
    return render_template('index.html', logo=logo)

@app.route('/play', methods=['GET', 'POST'])
def play_game():
    if request.method == 'GET':
        # Initialize the game
        user_cards.clear()
        computer_cards.clear()
        for _ in range(2):
            user_cards.append(deal_card())
            computer_cards.append(deal_card())

        return render_template('play.html', user_cards=user_cards, computer_card=computer_cards[0])

    if request.method == 'POST':
        # Handle user's actions (draw or pass)
        if request.form.get('action') == 'draw':
            user_cards.append(deal_card())
            user_score = calculate_score(user_cards)
            computer_score = calculate_score(computer_cards)

            if user_score > 21:
                return render_template('result.html', user_cards=user_cards, computer_cards=computer_cards, result="YOU WENT OVER! YOU LOSE!", 
                                        user_score=user_score, computer_score=computer_score)
            return render_template('play.html', user_cards=user_cards, computer_card=computer_cards[0])
        else:
            # Computer's turn to play
            while calculate_score(computer_cards) < 17:
                computer_cards.append(deal_card())
            
            user_score = calculate_score(user_cards)
            computer_score = calculate_score(computer_cards)
            result = compare(user_score, computer_score)

            return render_template('result.html', user_cards=user_cards, user_score=user_score, computer_score=computer_score, 
                                   computer_cards=computer_cards, result=result)

if __name__ == '__main__':
    app.run(debug=True)

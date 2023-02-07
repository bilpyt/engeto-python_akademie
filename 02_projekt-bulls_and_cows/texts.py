"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Jan Hlaváček
e-mail: jan@hlavackovi.net
discord: Jan H.#7413
"""

def text(which_text, iteration=None, b=None, c=None):
    """
    Funkce na vracení textových řetězců. Všechny texty jsou tak
    definovány na jednom místě.
    """
    if which_text == "greeting":
        print(f"Hi, player!")
    elif which_text == "start":
        print(f"I´ve generated a random 4 digit number for you.\n"
        "Let´s play a bulls and cows game.")
    elif which_text == "wrong_input":
        print(f"You don´t enter 4 digits number. Please enter number again.")
    elif which_text == "end":
        print(f"Thank you for the game.\nHave a nice day! ;-)")
    elif which_text == "line":
        print(45*"-")
    elif which_text == "ask_to_play_again":
        return "Do you want play again? Y/N\n"
    elif which_text == "ask_to_continue":
        return ("You are guessing very long.\n"
                "If you want to exit, type: X\n"
                "For continue press Enter.\n")
    elif which_text == "enter_number":
        return "Enter your number:\n>>> "
    elif which_text == "you_win_tip":
        return (f"Correct, you´ve guessed the right number"\
                f"\nin {iteration} guess. "\
                f"{'It is awesome!' if iteration < 5 else 'Good Job!'}")
    elif which_text == "attempt_bulls_cows":
        return (f"{iteration}. attempt - "
                f"{b} bull{'s' if b > 1 else ''}, "
                f"{c} cow{'s' if c > 1 else ''}")
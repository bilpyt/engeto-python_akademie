#!/bin/python3
"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Jan Hlaváček
e-mail: jan@hlavackovi.net
discord: Jan H.#7413

Texty jsou odděleny do samostatného souboru.
"""

from random import randint
from texts import text

def new_hidden_number():
    """
    Generování nového hádaného čísla
    """
    number = [0, 0, 0, 0]
    for i in range(4):
        while True:
            num = int(randint(0,9))
            if num in number or (num == 0 and i == 0):
                continue
            else:
                number[i] = num
                break
    return(number)


def assessment(tip_list, hidden_list):
    """
    Funkce na vydnocení jak tip odpovídá generovanému listu.
    Vrací zpět slovník s klíči "bulls" a "cows" a jednotlivými
    čísly k nim náležícími.
    """
    checked_indexes = [0, 0, 0, 0]
    bulls_and_cows = {"bulls": [], "cows": []}
    for x in range (0,4):
        if tip_list[x] == hidden_list[x]:
            bulls_and_cows["bulls"].append(tip_list[x])
            checked_indexes[x] = 1
    for i in range(0,4):
        if checked_indexes[i] != 1:
            for j in range(0,4):
                if checked_indexes[j] == 0:
                    if tip_list[i] == hidden_list[j] and checked_indexes[j] != 2:
                        bulls_and_cows["cows"].append(tip_list[i])
                        checked_indexes[j] = 2
                        break
    return bulls_and_cows    


def result(bulls_and_cows, iteration):
    """
    Funkce vracející textový výsledek k jednotlivým pokusům.
    """
    b = len(bulls_and_cows['bulls'])
    c = len(bulls_and_cows['cows'])
    if b == 4:
        return text("you_win_tip", iteration)
    else:
        return text("attempt_bulls_cows", iteration, b, c)

def game():
    """
    Funkce samotné hry - hádání jednoho čísla.
    """
    text("start")
    text("line")
    hidden_number = new_hidden_number()
    iteration = 0
    while True:
        tip = input(text("enter_number"))
        if not len(tip) == 4 or not tip.isdigit():
            text("wrong_input")
            continue
        iteration += 1
        tip_list = [int(x) for x in tip]
        bulls_and_cows = assessment(tip_list, hidden_number)
        print(result(bulls_and_cows, iteration))
        text("line")
        if len(bulls_and_cows["bulls"]) == 4:
            break
        else:
            if iteration % 5 == 0:
                ask_to_continue = input(text("ask_to_continue"))
                if ask_to_continue.capitalize() == "X":
                    break


if __name__ == "__main__":
    text("greeting")
    text("line")
    game()
    while True:
        ask_to_play_again = input(text("ask_to_play_again"))
        if ask_to_play_again.capitalize() == "Y":
            game()
        elif ask_to_play_again.capitalize() == "N":
            break
    text("line")
    text("end")
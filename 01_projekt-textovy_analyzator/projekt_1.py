#!/bin/python3
"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Jan Hlaváček
e-mail: jan@hlavackovi.net
discord: Jan H.#7413
"""
#Import šablony textu
from task_template import TEXTS

#Databáze loginů a pomocné proměnné
username_pass = {"bob": "123","ann": "pass123", "mike": "password123", "liz": "pass123"}
texts_quantity = len(TEXTS)
sep_len = 70
separator = sep_len*"="
prev_len = sep_len - 7

#Získání vstupů od uživatele
get_username = input("Zadej uživatelské jméno: ")
get_pass = input("Zadej heslo: ")

#Ověření jména a hesla
if username_pass.get(get_username) is None or username_pass.get(get_username) != get_pass:
    print("Uživatelské jméno, nebo heslo je neplatné. Ukončuji program.")
    exit()

#Uvítání
print("\n" + separator)
print(f"Vítej {get_username},".center(sep_len))
print(f"máme pro tebe k analýze {texts_quantity} texty/ů.".center(sep_len))
print(separator + "\n")

#Výpis ukázky text - není třeba - jen na okrasu...
print(f"|----+{(prev_len)*'-'}|")
print(f"|{'ID':^4}|{'Ukázka textu':^{prev_len}}|")
print(f"|----+{(prev_len)*'-'}|")
for id in range(0,texts_quantity):
    prev_text = TEXTS[id][0:prev_len - 5].replace('\n',' ')
    print(f"|{id:^4}| {prev_text:^{prev_len - 5}}... |")
print(f"|----+{(prev_len)*'-'}|")

#Získání vstupu - ID textu
get_text_id = input("\nZadej prosím ID textu k analýze: ")

#Kontrola vstupu
if get_text_id.isnumeric() is False or int(get_text_id) not in range(0,texts_quantity):
    print("Nebylo zadáno platné ID textu. Ukončuji program...")
    exit()

#############################
#Počítací jádro programu
#proměnná s textem a se slovama
chosen_text = TEXTS[int(get_text_id)]
chosen_text_words = chosen_text.replace(".","").replace(",","").split()

#Celkový počet slov
words_count = len(chosen_text_words)

#Počet slov začínajících velkým písmenem
words_title_count = 0
for word in chosen_text_words:
    if word.istitle():
        words_title_count += 1

#Počet slov psaných velkými písmeny
words_upper_count = 0
for word in chosen_text_words:
    if word.isupper() and word.isalpha():
        words_upper_count += 1

#Počet slov psaných malými písmeny
words_lower_count = 0
for word in chosen_text_words:
    if word.islower():
        words_lower_count += 1

#Počet čísel (ne cifer) a jejich součet,
digits_count = 0
digits_sum = 0
for digit in chosen_text_words:
    if digit.isdigit():
        digits_count += 1
        digits_sum += int(digit)

#Počítání četnosti
word_len_occurency = {}
for word in chosen_text_words:
    length = len(word)
    if length not in word_len_occurency:
        word_len_occurency[length] = 1
    else:
        word_len_occurency[length] += 1

###################################
# Výpis statistik
print()
print("Zvolený text obsahuje", words_count, "slov")
print("Počet slov začínajících velkým písmenem:", words_title_count)
print("Počet slov psaných kapitálkami:", words_upper_count)
print("Počet slov psaných malými písmeny:", words_lower_count)
print("Počet čísel v textu:", digits_count)
print("Součet všech čísel v textu:", digits_sum)
print()

# Zobrazení sloupcového grafu s reprezentací četnosti délky slov
print(f"|{'-'*36}|")
print(f"|{'Graf četnosti výskytu délky slov':^36}|")
print(f"|{'-'*7}+{'-'*20}+{'-'*7}|")
print(f"|{'Znaků':^7}|{'Výskyt':^20}|{'Počet':^7}|")
print(f"|{'-'*7}+{'-'*20}+{'-'*7}|")
for id in range(1,len(word_len_occurency)+1):
    if word_len_occurency.get(id) is not None:
        print(f"|{id:^7}|{'*'*word_len_occurency[id]:<20}|{word_len_occurency[id]:^7}|")
print(f"|{'-'*7}+{'-'*20}+{'-'*7}|")


import random 
import requests
from pprint import pprint

def ask_for_difficulty_lvl():
    difficulty_list = ['EASY', 'MEDIUM', 'HARD']
    while True:
        difficulty_inp = input(f'Choose difficulty level from the list: {difficulty_list} \n').upper()
        if difficulty_inp in difficulty_list:
            return difficulty_inp


def number_of_lives(difficulty_inp):
    if difficulty_inp == "EASY":
        lives = 15
        print(f"\nYou chose level {difficulty_inp} with {lives} lives.\n")
        return lives
    elif difficulty_inp == "MEDIUM":
        lives = 10
        print(f"\nYou chose {difficulty_inp} with {lives} lives.\n")
        return lives
    elif difficulty_inp == "HARD":
        lives = 5
        print(f"\nYou chose level {difficulty_inp} with {lives} lives.\n")
        return lives
        

def draw_a_word(difficulty_inp):
    f = open("countries-and-capitals.txt", "r")
    lines = f.readlines()
    result = []
    for x in lines:
        result.append(x.split('|')[0])
   # w miejsce | wstawiany jest przecinek
    if difficulty_inp == "EASY":
        word_to_guess = random.choice(result[0:25])
        return word_to_guess
    elif difficulty_inp == "MEDIUM":
        word_to_guess = random.choice(result[:50])
        return word_to_guess
    else:
        word_to_guess = random.choice(result)
        return word_to_guess


def is_a_letter(letter):
    try: 
        int(letter)
        return False
    except ValueError:
        if len(letter) == 1 and letter.isalpha() == True:
            return True
        else:
            return False


def ask_for_a_letter(already_tried_letters, doubled_letters):
    letter = input('\nPlease provide a letter or type a quit if you want to exit: ').lower()
    while True:
        if is_a_letter(letter):
            if letter in already_tried_letters: #sprawdza czy letter jest w zbiorze już użytych liter, jeśli tak to zwraca że już ją użyto
                print("\nAlready used letters:", (" ".join(already_tried_letters)))
                print(f"You already used {letter}.\n")
                doubled_letters.append(letter)
                return letter
            else:
                already_tried_letters.append(letter) # jeśli litery nie użyto wcześniej, dodaje ją do listy already_tried_letters i zwraca całą listę
                print("\nAlready used letters:", (" ".join(already_tried_letters)))
                print("\n")
                break
        elif letter.upper() == 'QUIT':
            end_game = "See you soon!"
            eg = requests.get(f'http://artii.herokuapp.com/make?text={end_game}')
            print(eg.text)
            return 'end'
        else:
            if len(letter) == 0:
                print("You did not provide any letter!\n")
                break
            else:
                print(f"Wrong you provied '{letter}'! You need to provide one letter!\n")
                break
    return letter 

# strip rozdziela kazda litere slowa
# zwraca odgadniete słowo zamienione na podłogi
def word_dashed(word_to_guess):
    word_list = list(word_to_guess.strip(""))
    word_list_encode = []
    for i in word_list:
        # jezeli element jest literą, zamieniamy go na podloge, w przeciwnym razie - element jest pusty
        # wstawiany jest pusty element
        if i.isalpha():
            word_list_encode.append(i.replace(i, "_")) 
        else:
            word_list_encode.append(i)
    return print(" ".join(word_list_encode))
#zwraca wyprintowane podlogi

# podmienia podlogi na odgadniete litery
def guessing(word_to_guess, already_tried_letters):
    word_list = list(word_to_guess.strip(""))
    word_list_encode = []
    tried_letters = ''.join(already_tried_letters)
    upper_tried_letters = tried_letters.upper()
    already_tried_letters_upper = list(upper_tried_letters)
    if word_list[-1]== " ":
        word_list.pop()
    for i in word_list:
        if i in already_tried_letters or not i.isalpha():
            word_list_encode.append(i) #zostaje to co jest, gdy i nie jest literą, lub jest w uzytym zbiorze
        elif i in already_tried_letters_upper:
            word_list_encode.append(i) #w przeciwnym razie zwracany jest uzupelniony
        else:
            word_list_encode.append(i.replace(i, "_"))
    return print(" ".join(word_list_encode))


def game_start():  
    game_menu = "Welcome to Hangman"
    r = requests.get(f'http://artii.herokuapp.com/make?text={game_menu}')
    print(r.text)
    already_tried_letters = []
    guessed_letters = []
    doubled_letters = []
    difficulty = ask_for_difficulty_lvl() #pozniej mozna dodac, ze po zgadnieciu slowa znowu wybieramy poziom trudnosci   
    secret_word = draw_a_word(difficulty)
    lives = number_of_lives(difficulty)
    word_dashed(secret_word)
#pyta o literę, a potem odpala funkcję guessing, która daną literkę wypisuje w haśle i potem pyta ponownie o literę 
# / trzeba będzie przerwać gdy będzie całe hasło odgadnięte lub wszystkie stacone życia
    while True:
        a = ask_for_a_letter(already_tried_letters, doubled_letters)
        if a == "end":
            break

        guessing(secret_word, already_tried_letters)  
        secret_list = list(secret_word.strip("").lower()) #lista stworzona z oddzielonych liter zgadniętego słowa
        secret_list.sort()
        for x in secret_list:
            secret_list.pop(0)
            if secret_list[0] != ' ':
                break

        while True:
            if a not in secret_list and is_a_letter(a) == True:
                if a not in doubled_letters:# jezeli litera nie znajduje sie w liscie slowa do odgadniecia i litera jest literą pojedyncza
                    lives -= 1    
                    warning = "You missed! Left lives: "
                    l = requests.get(f'http://artii.herokuapp.com/make?text={warning}{lives}')
                    print(l.text)
                    break
                else:
                    break
            elif a in secret_list:
                if a not in doubled_letters: 
                    warning = "You are correct! Left lives: "
                    l = requests.get(f'http://artii.herokuapp.com/make?text={warning}{lives}')
                    print(l.text)
                    guessed_letters.append(a)
                    break
                else:
                    break
            else:
                break

        if set(guessed_letters) == set(secret_list):
            play_again = input("\nCongratulations! You win!\nDo you want to play again? [y/n]: ").lower()
            if play_again == 'y':
                game_start()
            else:
                end_game = "See you soon!"
                eg = requests.get(f'http://artii.herokuapp.com/make?text={end_game}')
                print(eg.text)
                break
            
        elif lives == 0:
            play_again = input("\nYou lost!The word to guess is: {secret_word}\n Do you want to play again? [y/n]: ").lower()
            if play_again == 'y':
                game_start()
            else:
                end_game = "See you soon!"
                eg = requests.get(f'http://artii.herokuapp.com/make?text={end_game}')
                print(eg.text)
                break


if __name__ == "__main__":
    game_start()

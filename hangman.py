import random 
import requests
from pprint import pprint

def ask_for_difficulty_lvl():
    difficulty_list = ['EASY', 'MEDIUM', 'HARD']
    while True:
        difficulty_inp = input(f'Choose difficulty level from the list: {difficulty_list} ').upper()
        if difficulty_inp in difficulty_list:
            return difficulty_inp


def number_of_lives(difficulty_inp):
    if difficulty_inp == "EASY":
        lives = 14
        word_to_guess = "AAA"
        print("You choose EASY level with 14 lives")
        return lives and word_to_guess
    elif difficulty_inp == "MEDIUM":
        lives = 12
        word_to_guess = "AAABBB"
        print("You choose MEDIUM level with 12 lives")
        return lives and word_to_guess
    elif difficulty_inp == "HARD":
        lives = 10
        word_to_guess = "AAABBBCCC"
        print("You choose HARD level with 10 lives")
        return lives and word_to_guess
        
# strip rozdziela kazda litere slowa
def word_dashed(word_to_guess):
    word_list = list(word_to_guess.strip(""))
    word_list_two = []
    for i in word_list:
        if i.isalpha():
            word_list_two.append(i.replace(i, "_")) 
        else:
            word_list_two.append(i)
    return print(" ".join(word_list_two))
    
            
# PART 1 zrobione
# display a menu with at least 3 difficulty choices and ask the user
# to select the desired level
# sample data, normally the user should choose the difficulty


# STEP 2 zrobione
# based on the chosen difficulty level, set the values 
# for the player's lives
# word_to_guess = "Cairo" # sample data, normally the word should be chosen from the countries-and-capitals.txt
# lives = 5 # sample data, normally the lives should be chosen based on the difficulty


# funkcja otwiera plik txt, tworzy listę z 1 kolumny oraz zwraca jedną losową wartość z tej listy
#liczba państw to 183, pula musi być zalezna od poziomu trudnosci
def draw_a_word(difficulty_inp):
    f = open("countries-and-capitals.txt", "r")
    lines = f.readlines()
    result = []
    for x in lines:
        result.append(x.split('|')[0])
   # w miejsce | wstawiany jest przecinek
    if difficulty_inp == "EASY":
        word_to_guess = random.choice(result[:25])
        print(word_to_guess)
        return word_to_guess
    elif difficulty_inp == "MEDIUM":
        word_to_guess = random.choice(result[:50])
        return word_to_guess
    else:
        word_to_guess = random.choice(result)
        return word_to_guess

# STEP 3 zrobione
# display the chosen word to guess with all letters replaced by "_"
# for example instead of "Cairo" display "_ _ _ _ _"


# STEP 4 zrobione
# ask the user to type a letter
# here you should validate if the typed letter is the word 
# "quit", "Quit", "QUit", "QUIt", "QUIT", "QuIT"... you get the idea :)
# HINT: use the upper() or lower() built-in Python functions
def is_a_letter(letter):
    try: 
        int(letter)
        return False
    except ValueError:
        if len(letter) == 1:
            return True
        else:
            return False

def ask_for_a_letter():
    while True:
        letter = input('Please provide a letter: ')
        if is_a_letter(letter):
            if letter.upper() == 'QUIT':
                return print(None)
            else:
                #w tym przypadku następuje wybor dobrej litery - trzeba dodac co zwraca
                #np dodanie do pustego zbioru itp
                pass
                #return letter
        else:
            print(f"Wrong you provied '{letter}'! You need to provide one letter!")
            break
    
    

# STEP 5
# validate if the typed letter is already in the tried letters
# HINT: search on the internet: `python if letter in list`
# If it is not, than append to the tried letters
# If it has already been typed, return to STEP 5. HINT: use a while loop here
# already_tried_letters = [] # this list will contain all the tried letters


# STEP 6
# if the letter is present in the word iterate through all the letters in the variable
# word_to_guess. If that letter is present in the already_tried_letters then display it,
# otherwise display "_".


# if the letter is not present in the word decrease the value in the lives variable
# and display a hangman ASCII art. You can search the Internet for "hangman ASCII art",
# or draw a new beautiful one on your own.



# STEP 7
# check if the variable already_tried_letters already contains all the letters necessary
# to build the value in the variable word_to_guess. If so display a winning message and exit
# the app.
# If you still have letters that are not guessed check if you have a non negative amount of lives
# left. If not print a loosing message and exit the app.
# If neither of the 2 conditions mentioned above go back to STEP 4


def game_start():  
    while True: 
        game_menu = "Welcome to Hangman"
        r = requests.get(f'http://artii.herokuapp.com/make?text={game_menu}')
        print(r.text)
        # ten zbior nie wiem czy tutaj, czy w osobnej funkcji
        #already_tried_letters = []
        #to podobnie
        #users_word = []
        difficulty = ask_for_difficulty_lvl() #pozniej mozna dodac, ze po zgadnieciu slowa znowu wybieramy poziom trudnosci
        secret_word = draw_a_word(difficulty)
        lives = number_of_lives(difficulty)
        dash = word_dashed(secret_word)
        a = ask_for_a_letter()
        # wy przypadku, gdy dlugosc slowa wybranego przez program nie jest podanemu przez nas
        #bedziemy wciaz pytani o slowo
        # while len(secret_word) != len(users_word):
        #     ask = ask_for_a_letter(already_tried_letters)

        #konczymy dzialanie programu w przypadku podania quit - funkcja zwraca wtedy none == false
        if a == False:
            break

    # lives = xxx
    # l = requests.get(f'http://artii.herokuapp.com/make?text={lives}')

       

if __name__ == "__main__":
    game_start()

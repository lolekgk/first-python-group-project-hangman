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
        print(f"You choose EASY level with {lives} lives\n")
        return lives
    elif difficulty_inp == "MEDIUM":
        lives = 10
        print(f"You choose MEDIUM level with {lives} lives\n")
        return lives
    elif difficulty_inp == "HARD":
        lives = 5
        print(f"You choose HARD level with {lives} lives\n")
        return lives
        


def draw_a_word(difficulty_inp):
    f = open("countries-and-capitals.txt", "r")
    lines = f.readlines()
    result = []
    for x in lines:
        result.append(x.split('|')[0])
   # w miejsce | wstawiany jest przecinek
    if difficulty_inp == "EASY":
        word_to_guess = random.choice(result[19:21])
        #sprawdzenie slowa - usunac pozniej printa
        print(word_to_guess)
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
        if len(letter) == 1:
            return True
        else:
            return False


def ask_for_a_letter(already_tried_letters):
    letter = input('Please provide a letter or type a quit if you want to exit: \n').lower()
    while True:
        if is_a_letter(letter):
            if letter in already_tried_letters: #sprawdza czy letter jest w zbiorze już użytych liter, jeśli tak to zwraca że już ją użyto
                print("Already used letters: ", (" ".join(already_tried_letters)))
                print(f"You already used {letter}.\n")
                return letter
            else:
                already_tried_letters.append(letter) # jeśli litery nie użyto wcześniej, dodaje ją do listy already_tried_letters i zwraca całą listę
                print("Already used letters: \n", (" ".join(already_tried_letters)))
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
    word_list = list(word_to_guess.strip("").lower())
    word_list_encode = []
    if word_list[-1]== " ":
        word_list.pop()
    for i in word_list:
        if i in already_tried_letters or not i.isalpha():
            word_list_encode.append(i) #zostaje to co jest, gdy i nie jest literą, lub jest w uzytym zbiorze
        else:
            word_list_encode.append(i.replace(i, "_")) #w przeciwnym razie zwracany jest uzupelniony
    return print(" ".join(word_list_encode))

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
    game_menu = "Welcome to Hangman"
    r = requests.get(f'http://artii.herokuapp.com/make?text={game_menu}')
    print(r.text)
    already_tried_letters = []
    guessed_letters = []
    difficulty = ask_for_difficulty_lvl() #pozniej mozna dodac, ze po zgadnieciu slowa znowu wybieramy poziom trudnosci   
    secret_word = draw_a_word(difficulty)
    # secret_word = "Test"
    lives = number_of_lives(difficulty)
    word_dashed(secret_word)
#pyta o literę, a potem odpala funkcję guessing, która daną literkę wypisuje w haśle i potem pyta ponownie o literę 
# / trzeba będzie przerwać gdy będzie całe hasło odgadnięte lub wszystkie stacone życia
    while True: 
        a = ask_for_a_letter(already_tried_letters)
        guessing(secret_word, already_tried_letters)  
        secret_list = list(secret_word.strip("").lower()) #lista stworzona z oddzielonych liter zgadniętego słowa
        if a == 'end': #zakonczenie programu w przypadku wpisania quit
            break
        secret_list.sort()

        for x in secret_list:
            secret_list.pop(0)
            if secret_list[0] != ' ':
                break
        # if secret_list[0]== " ":
        #     secret_list.pop(0)
        # if secret_list[0]== " ":
        #     secret_list.pop(0)
        while True:
            if a not in secret_list and is_a_letter(a) == True: # jezeli litera nie znajduje sie w liscie slowa do odgadniecia i litera jest literą pojedyncza
                lives -= 1    
                warning = "You missed! Left lives: "
                l = requests.get(f'http://artii.herokuapp.com/make?text={warning}{lives}')
                print(l.text)
                print(f"You missed! Left lives: {lives}")
                break
            elif a in secret_list:  
                warning = "You are correct! Left lives: "
                l = requests.get(f'http://artii.herokuapp.com/make?text={warning}{lives}')
                print(l.text)
                guessed_letters.append(a)
                break
            #break
        #tutaj mozna dodać warunek z rozpoczęciem gry po wygranej/przegranej
    
        if set(guessed_letters) == set(secret_list):
            print("Congratulations! You win!\n")
            break
        elif lives == 0:
            print("You lost!\n")
            break


if __name__ == "__main__":
    game_start()

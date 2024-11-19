import requests
import random

# creating a random list of words using ChatGPT
random_list = ["apple", "breeze", "crystal", "diamond", "elephant", "forest", "galaxy", "horizon", "iceberg", "journey", "kangaroo", "lantern", "mountain", "nebula", "ocean", "piano", "quantum", "rainbow", "sunshine", "thunder", "umbrella", "volcano", "waterfall", "xylophone", "zebra", "anchor", "bicycle", "cloud", "desert", "eclipse", "feather", "glacier", "hammock", "island", "jungle", "koala", "lighthouse", "meadow", "nightfall", "oasis", "penguin", "quiver", "river", "starfish", "tornado", "unicorn", "valley", "whale", "xenon", "yogurt", "zephyr"]

def get_random_word_api():
    # first trying to get a word from an API server
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            return response.json()[0]
        else:
            print("Failed to fetch word from API. Using fallback method.")
    except requests.RequestException:
        print("Error connecting to the API. Using fallback method.")
    
    # if the first method is not working, we get a random word from the list provided
    return random.choice(random_list)


# creating a dictionary of the hangman stages
hangman_wrongs = {
                1: (" o ",
                    "   ",
                    "   "),
                2: (" o ",
                    " | ",
                    "   "),
                3: (" o ",
                    "/|  ",
                    "   "),
                4: (" o ",
                    "/|\\",
                    "   "),
                5: (" o ",
                    "/|\\ ",
                    "/  "),
                6: (" o ",
                    "/|\\ ",
                    "/ \\"),   }

# creating a function to mask the given word
def mask_word(word):
    return "*" * len(word)

# a function that shows the guessed letters
def letters_guess(letter, word, guess_word):
    copy = list(guess_word)

    # whenever a letter is guesed we will display every apparition of it
    for index, char in enumerate(word):
        if char == letter:
            copy[index] = letter
    
    updated_copy = ''.join(copy)
    
    # if the masked word isnn't change (meaning the letter was wrong) the function will return a False statement
    if updated_copy == guess_word:
         return False
    # if the masked word is identical to the word that need to pe guessed the function will return a True statement
    elif updated_copy == word:
         return True
    # if the letter was guessed corectly we will modify the masked word
    else:
         guess_word = updated_copy
         return guess_word
    
   
               
  
# generating the word that will be guessed
word =  get_random_word_api()
# masking that word and printing it
maskedWord = mask_word(word)
print(maskedWord)

# initializing the number of wrongly guessed letters
wrongs = 0

while wrongs<6:
    # getting the guessed letter
    player_input = input("Enter the letter: ")
    # if the word was guessed corectly we will show a message and stop the while() function
    if letters_guess(player_input, word, maskedWord) == True:
        print(f"Congratulation! The word is {word}.")
        break
    else:
        # showing the hangman state whenever a mistake is made, and incrementing the number of it
        if letters_guess(player_input, word, maskedWord) == False:
            wrongs += 1
            if(wrongs < 6):
                for line in hangman_wrongs[wrongs]:
                    print(line)

                print(maskedWord)
                letters_guess(player_input,word,maskedWord)
        else:
            # continuing the game until the number is guessed or the game is over
            maskedWord = letters_guess(player_input,word,maskedWord)
            print(maskedWord)
            print("Please entry next letter!")
            letters_guess(player_input,word,maskedWord)

# if the player made 6 mistakes, the game is over
if wrongs == 6:
    list(map(lambda line: print(line), hangman_wrongs[6]))
    print(f"Game over! The word was {word}")


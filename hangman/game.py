import random
from .exceptions import *

# Complete with your own, just for fun :)
LIST_OF_WORDS = []


def _get_random_word(list_of_words):
    if not list_of_words:
        raise InvalidListOfWordsException("List of words is empty or None.")
    return random.choice(list_of_words)


def _mask_word(word):
    if not word or not isinstance(word, str):
        raise InvalidWordException("Invalid word provided.")
    return '*' * len(word)


def _uncover_word(answer_word, masked_word, character):
    if len(answer_word) != len(masked_word):
        raise InvalidWordException("Answer word and masked word lengths do not match.")
    
    if not character or len(character) != 1 or not character.isalpha():
        raise InvalidGuessedLetterException("Invalid guessed letter.")
    
    new_masked = list(masked_word)
    for index, char in enumerate(answer_word):
        if char.lower() == character.lower():
            new_masked[index] = char
    
    return ''.join(new_masked)


def guess_letter(game, letter):
    if game['masked_word'] == game['answer_word'] or game['remaining_misses'] == 0:
        raise GameFinishedException("Game has already finished.")
    
    if letter in game['previous_guesses']:
        raise InvalidGuessedLetterException("Letter has already been guessed.")
    
    game['previous_guesses'].append(letter)
    
    if letter.lower() in game['answer_word'].lower():
        game['masked_word'] = _uncover_word(game['answer_word'], game['masked_word'], letter)
        
        if game['masked_word'] == game['answer_word']:
            raise GameWonException("Congratulations! You've won the game!")
    else:
        game['remaining_misses'] -= 1
        
        if game['remaining_misses'] == 0:
            raise GameLostException("Sorry, you've lost the game.")
    
    return game


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game

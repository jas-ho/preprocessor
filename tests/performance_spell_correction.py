from context import spell_correct_word, spell_correct_text, spell_correct
from context import misspell_word
# this script measures the performance of the spell checker by
#  - choosing a word from a list of correct German words
#  - applying a random misspelling to it
#  - comparing the top suggestion from spell_correct_word to the correct word
#
#  the success rate is defined as observed frequency of words where
#   the top suggestion after the random misspelling is equal to the input word

import os
import pickle
import random


# load correct words
test_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(test_dir, '..'))
data_dir = os.path.join(module_dir, 'data')

file = os.path.join(data_dir, 'pickles', 'correct_words.pickle')
with open(file, 'rb') as f:
    correct_words = pickle.load(f)

assert len(correct_words) == 22390


# measure performance of spellchecker on randomly chosen subset of correct words
random.shuffle(correct_words)
test_words = correct_words[:100]

best_suggestion = lambda word: spell_correct_word(word)[0]
## uncomment the following to demonstrate that all test words are recognizedd
##  if we don't introduce additional misspellings
# suggestions = list(map(best_suggestion, test_words))
# assert suggestions == test_words
# print ('Without introducing misspellings all test words are recognized.')

# a single error introduced
test_words_1 = map(misspell_word, test_words)
suggestions1 = map(best_suggestion, test_words_1)
successes1 = map((lambda x, y: x==y), suggestions1, test_words)
rate1 = sum(successes1)
assert len(test_words) == 100
print ("Single random misspelling: success rate = {}%".format(rate1))

# a second error introduced
test_words_2 = map(misspell_word, map(misspell_word, test_words))
suggestions2 = map(best_suggestion, test_words_2)
successes2 = map((lambda x, y: x==y), suggestions2, test_words)
rate2 = sum(successes2)
assert len(test_words) == 100
print ("Two random misspellings: Success rate = {}%".format(rate2))

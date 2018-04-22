# this is a python script for
#  - generating a list of correct words according to the hunspell-dict
#  - exporting it to a pickle inside ../data/pickles/
#
#  this list can be used for benchmarking the spellchecker
#

import os
import pickle

script_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(module_dir, 'data')


# read list of words from  hunspell/de_DE.dic to generate test cases for the spell checker
# build dict of words (as keys) and affixes (as items)
hunspell_words = dict()
hunspell_dic_file = os.path.join(data_dir,'hunspell','de_DE.dic')
with open(hunspell_dic_file, encoding="Windows 1252") as f:
    [next(f) for k in range(15)] # first 15 lines are header --> skip them
    for line in f:
        if 'ä/n'==line.rstrip(): # end of 'stand-alone-words'
            break
        components = line.rstrip().split('/') # most lines contain additional info separated by '/'
        word = components[0]
        affix = (components[1] if len(components)>1 else '')
        hunspell_words[word]=affix

# unit tests: the following should be in the list
assert 'Abk.' in hunspell_words
assert 'Äbte' in hunspell_words
assert 'Zyste' in hunspell_words


# filter hunspell_words for certain affixes to generate list of correct words
correct_words = []
for word, affix in hunspell_words.items():
    if 'd' in affix or 'hij' in affix:
        # affix 'd' seems to mark misspelled words
        # affix 'hij' seems to mark common prefixes
        pass
    else:
        correct_words.append(word)

# unit tests: the following words should have been excluded
in_hunspell_but_incorrect = lambda word: (word in hunspell_words) and (word not in correct_words)
assert in_hunspell_but_incorrect('Ährenamt')
assert in_hunspell_but_incorrect('Änderungs')
assert in_hunspell_but_incorrect('Abbildungs')
assert in_hunspell_but_incorrect('Zwergfell')
assert in_hunspell_but_incorrect('Zwischen')


# export this list for future reference
out_file = os.path.join(data_dir, 'pickles', 'correct_words.pickle')
with open(out_file, 'wb') as f:
    pickle.dump(correct_words, f)


# unit test: check that export worked
with open(out_file, 'rb') as f:
    correct_words2 = pickle.load(f)
assert correct_words2 == correct_words

# print(correct_words)
print('Exported list of correct German words to: \n{}'.format(out_file))

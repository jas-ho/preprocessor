# This script reads in the training data obtained from the TIGER corpus
#  (as produced by the script create_TIGER_test_train_data.py)
# It builds a simple dictionary for lemmata lookup
#  (to be used inside lemmatization.py)
#  and stores it as a pickle in ../data/pickles/
#  (following https://github.com/WZBSocialScienceCenter/germalemma.git)

import os
import pickle
import itertools

import nltk
import codecs
import random
from collections import Counter

print('Building a lemmata dictionary from the TIGER training data...')
# read training data from TIGER-corpus
#  format is: [
#  [ (word1, pos1, lemma1), (word2, pos2, lemma2)], # first sentence
#  [ (word1, pos1, lemma1), (word2, pos2, lemma2)], # second sentence
#   ...]
script_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(module_dir, 'data')

train_file = os.path.join(data_dir, 'pickles', 'TIGER_train.pickle')
assert os.path.isfile(train_file), \
    """TIGER-corpus-training data not found.
    To create the required test-data, please run create_TIGER_test_train_data.py"""

with open(train_file, 'rb') as f:
    train_sents = pickle.load(f)


# only need token and lemma
#  --> discard POS-tags
def remove_POS(sents):
    # only first (word) and second entry (POS-tag) for each tuple are of interest
    first_last = (lambda mytuple: (mytuple[0], mytuple[2]))
    return list(map((lambda mylist: list(map(first_last, mylist))), sents))

train_sents = remove_POS(train_sents)


# lemmata are assigned on a word-by-word basis
#  --> no need to take the sentence structure into account
#  --> make a big list of all tuples
train_words = itertools.chain.from_iterable(train_sents)


# turn this into a dict
lemmata_dict = dict(train_words)
assert lemmata_dict['des'] == 'der'
assert lemmata_dict['die'] == 'der'

# export it for later reuse
lemmata_file = os.path.join(data_dir, 'pickles', 'lemmata.pickle')
with open(lemmata_file, 'wb') as f:
    pickle.dump(lemmata_dict, f)

# unit test: check that export worked
with open(lemmata_file, 'rb') as f:
    lemmata_dict2 = pickle.load(f)
assert lemmata_dict2 == lemmata_dict
print('Exported the lemmata dictionary to: \n{}\n'.format(lemmata_file))

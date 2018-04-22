# this script reads in the TIGER corpus and divides it randomly in two sets:
# -  training set (80% of the data)
# -  testing set (20% of the data)
# these sets will be stored in ../data/pickles.. for later usage for
# -  training the POS-tagger and the lemmatizer
# -  testing the POS-tagger and the lemmatizer

import nltk
import os
import pickle
import codecs
import random
from collections import Counter

# read tokens, pos, and lemmata sentence-wise from from TIGER-corpus
#  (inspired by https://github.com/WZBSocialScienceCenter/germalemma.git)
script_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(module_dir, 'data')

tiger_file = os.path.join(data_dir,
    'tiger_release_aug07.corrected.16012013.conll09')
assert os.path.isfile(tiger_file), \
    """TIGER-corpus-file not found.
    To create the required test-data, please
     1) download {} and
     2) unpack into {}""".format(
        "http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/download/tigercorpus-2.2.conll09.tar.gz",
        data_dir)

# note: sentences are delimited by blank lines in tiger_file
tagged_words = []
tagged_sents = []
with codecs.open(tiger_file, encoding="utf-8") as f:
    print('Loading TIGER-corpus...')
    for line in f:
        if not line.strip():
            # line is empty --> start a new sentence
            tagged_sents.append(tagged_words)
            tagged_words = []
        else:
            # line is not empty --> append to old sentence
            parts = line.split()
            assert len(parts) == 15
            token, lemma = parts[1:3]
            pos = parts[4]
            tagged_words.append((token, pos, lemma))
    print ('Done.\n')


# caution: sentences in tagged_sents are not unique
tagged_sents_unique = set(tuple(tagged_sent) for tagged_sent in tagged_sents) # new format (set of tuples)
tagged_sents_unique = list(map(list, tagged_sents_unique)) # revert to original format (list of lists)
print ("{}% out of the {} sentences in the TIGER corpus are unique.".format(
    int(100*len(tagged_sents_unique)/len(tagged_sents)),
    len(tagged_sents)))


# checking that it worked as expected: every sentence appears exactly once
assert set([1])==set(Counter(map(tuple, tagged_sents_unique)).values())
print ("Duplicate sentences removed.\n")


# randomize order
random.shuffle(tagged_sents)
tagged_sents[0]


# split into test and training
split_ind = int(0.2 * len(tagged_sents))
test_sents, train_sents = tagged_sents[:split_ind], tagged_sents[split_ind:]

# export this list for future reference
train_file = os.path.join(data_dir, 'pickles', 'TIGER_train.pickle')
test_file = os.path.join(data_dir, 'pickles', 'TIGER_test.pickle')

with open(train_file, 'wb') as f:
    pickle.dump(train_sents, f)

with open(test_file, 'wb') as f:
    pickle.dump(test_sents, f)


# unit test: check that export worked
with open(train_file, 'rb') as f:
    train_sents2 = pickle.load(f)
assert train_sents2 == train_sents

with open(test_file, 'rb') as f:
    test_sents2 = pickle.load(f)
assert test_sents2 == test_sents

# print(correct_words)
print('Exported training data to: \n{}\n'.format(train_file))
print('Exported testing data to: \n{}\n'.format(test_file))

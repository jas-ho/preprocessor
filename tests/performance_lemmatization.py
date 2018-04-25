import os
import pickle
import random

from context import lemmatize_word
from context import data_dir
from context import words_detokenize

# this script measures the performance of the lemmatizer
#  on test data from the TIGER corpus

# load test_data
test_file = os.path.join(data_dir, 'pickles', 'TIGER_test.pickle')
with open(test_file, 'rb') as f:
    test_sents = pickle.load(f)

# loop over test data
word_no = 0
success_no = 0
for lemmatized_sent in test_sents:
    word_no += len(lemmatized_sent)
    for word, POStag, lemma in lemmatized_sent:
        __, lemma_out = lemmatize_word((word, POStag))
        if lemma==lemma_out:
            success_no += 1

print('{} out of {} words in the test set were correctly lemmatized.'.format(
    success_no, word_no))
print('Success rate: {}%'.format(round(100*success_no/word_no)))

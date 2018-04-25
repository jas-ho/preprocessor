import os
import pickle
import random

from context import pos_tag_sentence
from context import data_dir
from context import words_detokenize

# this script measures the performance of the POS-tagger
#  on test data from the TIGER corpus

# load test_data
train_file = os.path.join(data_dir, 'pickles', 'TIGER_train.pickle')
with open(train_file, 'rb') as f:
    train_sents = pickle.load(f)

def remove_lemma(sents):
    # only first (word) and second entry (POS-tag) for each tuple are of interest
    firsttwo = (lambda mytuple: mytuple[:2])
    return list(map((lambda mylist: list(map(firsttwo, mylist))), sents))

train_sents = remove_lemma(train_sents)

# loop over test data
tag_no = 0
success_no = 0
for tagged_sent in train_sents[:1000]:
    sent, tags = zip(*tagged_sent)
    tagged_sent_out = pos_tag_sentence(words_detokenize(sent))
    sent_out, tags_out = zip(*tagged_sent_out)
    successes = map((lambda x, y: x==y), tags, tags_out)

    tag_no += len(tags)
    success_no += sum(successes)

print('{} out of {} words in the test set were correctly POS-tagged.'.format(
    success_no, tag_no))
print('Success rate: {}%'.format(round(100*success_no/tag_no)))

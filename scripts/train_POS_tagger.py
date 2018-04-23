# load POS-tagger for German
import os
import pickle
import random
from nltk import word_tokenize
from context import ClassifierBasedGermanTagger as CBGT


# load training data
script_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(module_dir, 'data')

train_file = os.path.join(data_dir, 'pickles', 'TIGER_train.pickle')
print('Loading training data from \n{}...'.format(train_file))
with open(train_file, 'rb') as f:
    train_sents = pickle.load(f)
print('Done.\n')

# split into dev-train and dev-test sets
random.shuffle(train_sents)
split_ind = int(0.1 * len(train_sents))
train_sents_devtest = train_sents[:split_ind]
train_sents_train = train_sents[split_ind:]

def remove_lemma(sents):
    # only first (word) and second entry (POS-tag) for each tuple are of interest
    firsttwo = (lambda mytuple: mytuple[:2])
    return list(map((lambda mylist: list(map(firsttwo, mylist))), sents))

train_sents_train = remove_lemma(train_sents_train)
train_sents_devtest = remove_lemma(train_sents_devtest)


# train the tagger
print('Training the tagger...')
tagger = CBGT.ClassifierBasedGermanTagger(train=train_sents_train)
print('Done.\n')

# test the tagger systematically
print('Evluating performance of the tagger on dev-test-set...')
devaccuracy = tagger.evaluate(train_sents_devtest)
print('Done. Accuracy: {}%.\n'.format(int(100 * devaccuracy)))  # roughly 93%


# TO DO: debugging and improvements of the tagger
#  based on typical errors observed in the devtest-set
#  .....
#  more or less as follows:
#
verbose = False
from collections import Counter
POStag_false_friends = Counter()
POStag_missed_sents = []
# contains pairs (tag_guessed, tag_correct) of tags where
# - the first one was incorrectly chosen by the POS-tagger
# - the second one is the correct POS-tag according to TIGER-corpus annotation
for (ind, tagged_sent) in enumerate(train_sents_devtest[:20]):
    sent, POStags_correct = zip(*tagged_sent)
    sent, POStags_guessed = zip(*tagger.tag(sent))
    if not (POStags_guessed == POStags_correct):
        POStag_missed_sents.append(ind)
        for (guessed, correct) in zip(POStags_guessed, POStags_correct):
            if not guessed == correct:
                POStag_false_friends[(guessed, correct)] += 1
                if verbose:
                    print("\ninput:\n", sent)
                    print("\ntags (guessed):\n", POStags_guessed)
                    print("\ntags (TIGER-corpus):\n", POStags_correct)
                    print("\ntag (guessed):\n", guessed)
                    print("\ntag (TIGER-corpus):\n", correct)
                    print()


# retrain the tagger using the whole training_set
print('Retraining the tagger using all training data...')
tagger = CBGT.ClassifierBasedGermanTagger(train=train_sents_train+train_sents_devtest)
print('Done.\n')


# test the tagger on single cases
assert tagger.tag(word_tokenize("Was für ein schöner Tag.")) == \
                                            [('Was', 'PWS'),
                                             ('für', 'APPR'),
                                             ('ein', 'ART'),
                                             ('schöner', 'ADJA'),
                                             ('Tag', 'NN'),
                                             ('.', '$.')]

# save the tagger for later reuse
tagger_file = os.path.join(data_dir, 'pickles', 'POStagger.pickle')
with open(tagger_file, 'wb') as f:
    pickle.dump(tagger, f)

# unit test: check that export worked
with open(tagger_file, 'rb') as f:
    tagger2 = pickle.load(f)
assert tagger2.tag(word_tokenize("Was für ein schöner Tag.")) == \
                                            [('Was', 'PWS'),
                                             ('für', 'APPR'),
                                             ('ein', 'ART'),
                                             ('schöner', 'ADJA'),
                                             ('Tag', 'NN'),
                                             ('.', '$.')]

print('Exported POStagger to: \n{}\n'.format(tagger_file))

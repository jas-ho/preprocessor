import os
import pickle
import json

try:
    lemmata_dict
except:
    # load lemmata_dict
    file_dir = os.path.abspath(os.path.dirname(__file__))
    module_dir = os.path.abspath(os.path.join(file_dir, '..'))
    data_dir = os.path.join(module_dir, 'data')

    tagger_file = os.path.join(data_dir, 'pickles', 'lemmata.pickle')
    with open(tagger_file, 'rb') as f:
        lemmata_dict = pickle.load(f)


### suffix-dict copied from https://github.com/WZBSocialScienceCenter/germalemma/blob/master/germalemma.py
# German language adjective suffixes
ADJ_SUFFIXES_BASE = (
    'bar',
    'haft',
    'ig',
    'isch',
    'lich',
    'los',
    'sam',
    'en',
    'end',
    'ern'
)

ADJ_SUFFIXES_FLEX = (
    'e',
    'er',
    'es',
    'en',
    'em',
    'ere',
    'erer',
    'eres',
    'eren',
    'erem',
    'ste',
    'ster',
    'stes',
    'sten',
    'stem',
)

ADJ_SUFFIXES_DICT = {}

for suffix in ADJ_SUFFIXES_BASE:
    for flex in ADJ_SUFFIXES_FLEX:
        ADJ_SUFFIXES_DICT[suffix + flex] = suffix
###

# MAIN FUNCTION #
def lemmatize(json_in, output_file=None):
    """
    Takes a json-like dict as produced by pos_tag and adds lemmatization

    Arguments:
        json_in {dict} -- json-like dict as produced by pos_tag

    Keyword Arguments:
        output_file {str} -- If provided, output is also written to this file
         (default: None)
    """
    sents = json_in.keys()
    json_out = json_in.copy()
    for sent in sents:
        corrections = json_out[sent]["spellingcorrections"]
        for corr in corrections:
            corr_sent = list(corr.keys())[0]
            corr_dict = corr[corr_sent]
            tagged_sent = corr_dict["postagger"]

            # revert to useful format: list of tuples
            tagged_sent = [list(dic.items())[0] for dic in tagged_sent]
            lemmatized_sent = lemmatize_sentence(tagged_sent)
            ls_list_of_dicts = [{tok: pos} for (tok, pos) in lemmatized_sent]
            corr_dict["lemmatization"] = ls_list_of_dicts

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(json_out, f)

    return json_out


def lemmatize_sentence(postagged_sent):
    """Apply lemmatize_word to each word in a POS-tagged sentence."""
    lemmatized_sent = map(lemmatize_word, postagged_sent)
    return list(lemmatized_sent)


def lemmatize_word(postagged_word):
    """Try to lemmatize the word using different methods.
    - direct lookup from a dictionary based on part of the TIGER corpus
    - ...."""
    word, POStag = postagged_word

    # first: try lookup in lemmata dictionary
    lemma = lemmata_lookup(word)
    if lemma:
        return (word, lemma)

    # next: if the word is an adjective try to find its base form
    if POStag.startswith('ADJ'):
        lemma = lemmata_adjective(word)
        if lemma:
            return (word, lemma)

    # if no method was successful
    return (word, '???')


# AUXILIARY FUNCTIONS #
def lemmata_lookup(word):
    """Try to find the word in the lemmata dictionary"""
    if word in lemmata_dict:
        return lemmata_dict[word]
    else:
        return None


def lemmata_adjective(word):
    """Try to find suffix of word in dict and return its base form"""
    # taken from germalemma.py
    for full, reduced in ADJ_SUFFIXES_DICT.items():
        if word.endswith(full):
            lemma = (word[:-len(full)] + reduced).lower()
            return lemma

    return None

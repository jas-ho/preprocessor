import os
import pickle
import json
from nltk import word_tokenize
from .context import ClassifierBasedGermanTagger as CBGT

try:
    tagger
except:
    # load POS-tagger
    file_dir = os.path.abspath(os.path.dirname(__file__))
    module_dir = os.path.abspath(os.path.join(file_dir, '..'))
    data_dir = os.path.join(module_dir, 'data')

    tagger_file = os.path.join(data_dir, 'pickles', 'POStagger.pickle')
    with open(tagger_file, 'rb') as f:
        tagger = pickle.load(f)


# MAIN FUNCTION #
def pos_tag(json_in, output_file=None):
    """
    Takes a json-like dict as produced by spell_correct and adds POS-tags

    Arguments:
        json_in {dict} -- json-like dict as produced by spell_correct

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
            tagged_sent = pos_tag_sentence(corr_sent)
            corr_dict = corr[corr_sent]
            corr_dict["postagger"] = dict(tagged_sent)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(json_out, f)

    return json_out


def pos_tag_sentence(sent):
    """
    Takes a sentence "word1 word2 ..."
    and returns a pos-tagged version of the form
    [(word1, POStag1), (word2, POStag2),...]
    """
    return tagger.tag(word_tokenize(sent))

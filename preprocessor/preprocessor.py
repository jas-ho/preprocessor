import os
import json
import pickle

from .spell_correction import spell_correct
from .pos_tagging import pos_tag
from .lemmatization import lemmatize

def preprocess(json_in, max_suggestions=2, output_file=None):
    """
    Takes a json-file with a list German sentences for NLP-preprocessing.
    Performs spell-correction, POS-tagging and lemmatization.
    Returns a json-like dict.

    Expected json-format for the input:
    - a single key: "input"
    - corresponding value: list of German input sentences s1, s2,... :str.

    Output:
    json-compatible dict of the form
    {s1: {
        "spellingcorrections": [
        {
            suggestion1: {
                "confidence": confidence1,
                "postagger": {word1: postag1, word2: postag2,...}
                "lemmatization": {word1: lemma1, word2: lemma2,...}
                },
            suggestion2: {
                "confidence": confidence2,
                "postagger": {...}
                "lemmatization": {...}
            },
            ....
        }

        }],
    s2: {...},
    ...
    }

    Arguments:
        json_in {str} -- path to input json-file.

    Keyword Arguments:
        max_suggestions {number} -- max. number suggested corrections per sentence
         (default: {10})
        output_file {str} -- If provided, output is also written to this file
         (default: None)
    """
    json_spelled = spell_correct(json_in, max_suggestions=max_suggestions)
    json_tagged = pos_tag(json_spelled)
    json_out = lemmatize(json_tagged)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(json_out, f)

    return json_out

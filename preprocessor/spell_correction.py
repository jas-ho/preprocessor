import hunspell
import os
import itertools
import json
from numpy import prod


# MAIN FUNCTION #
def spell_correct(json_file, max_suggestions=2, output_file=None):
    """
    Take path to json-file with German sentences to be corrected.
    Expected json-format:
    - a single key: "input"
    - corresponding value: list of German input sentences s1, s2,... :str.

    Return json-compatible dict of the form
    {s1: {
        "spellingcorrections": [
        {
            suggestion1: {
                "confidence": confidence1
                },
            suggestion2: {
                "confidence": confidence2
            },
            ....
        }

        }],
    s2: {...},
    ...
    }

    list of autocorrected sentences sorted by confidence
    of automatic spell correction (best one first).

    Return corresponding confidences as second return argument.

    Arguments:
        json_file {str} -- path to input json-file.

    Keyword Arguments:
        max_suggestions {number} -- max. number of returned sentences
         (default: {10})
        output_file {str} -- If provided, output is also written to this file
         (default: None)
    """
    json_input = json.load(open(json_file))
    keys = list(json_input.keys())
    assert keys == ['input'], \
        'Unexpected keys "{}" in input file. Expected only "input"'.format(
            keys)

    input_sents = json_input['input']
    json_output = {}
    for sent in input_sents:
        suggs, confs = spell_correct_text(sent, max_suggestions=max_suggestions)
        all_corrections = []
        for (sugg, conf) in zip(suggs, confs):
            all_corrections.append({sugg: {"confidence": conf}})
        json_output[sent] = {"spellingcorrections": all_corrections}

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(json_output, f)

    return json_output


def spell_correct_text(text, flag_corrected=False, max_suggestions=10):
    """
    Take `text` and return
    - list of suggested spelling corrections (:str) for `text`
    - list of confidences (:float) in the corresponding correction.

    max_suggestions (default: 10): maximum number of returned suggestions

    If `flag_corrected` is True (default: False):
    Surround corrected words  with '*'.
    ("corrected words" are suggested words which are not equal to input word)
    """
    suggs = []
    confs = []

    for word in word_tokenize(text):
        # if we return at most max_suggestions sentences
        #  we need at most max_suggestions suggestions per word
        sugg, conf = spell_correct_word(word, return_confidences=True,
                                        max_suggestions=max_suggestions)
        suggs.append(sugg)
        confs.append(conf)

    # all suggested sentences are obtained by
    #  detokenizing the Cartesian product of
    #  the list of all suggestions per word
    suggs = [words_detokenize(sent_list)
             for sent_list in itertools.product(*suggs)]

    # corresponding confidences are obtained by
    #  multiplying the confidences for each word
    confs = [prod(conf_list)
             for conf_list in itertools.product(*confs)]

    # sort suggestions and confidences by confidence
    confs, suggs = zip(*sorted(zip(confs, suggs), reverse=True))
    confs = list(confs)
    suggs = list(suggs)

    return suggs[:max_suggestions], confs[:max_suggestions]


def spell_correct_word(word, flag_corrected=False,
                       return_confidences=False, max_suggestions=10):
    """
    Take `word` and return a list of spell-corrected versions of `word`.
    If `word` is correctly spelled, return [`word`].

    max_suggestions (default: 10): maximum number of returned suggestions

    If `return_confidences` is True (default: False):
    Return list of confidences (floats between zero and 1) as second output.

    If `flag_corrected` is True (default: False):
    Surround corrected words  with '*'.
    ("corrected words" are suggested words which are not equal to input word)
    """
    if word in ['.', ',', '!', '?', '"']:
        # no attempt to correct punctuation marks
        if return_confidences:
            return [word], [1.]
        else:
            return word

    spell_is_correct = spellchecker.spell(word)

    if spell_is_correct:
        suggs = [word]  # suggs: list of suggestions to be returned
        confs = [1.]    # confs: list of confidences to be returned
    else:
        suggs = []
        confs = []

    spell_suggs = spellchecker.suggest(word)
    if spell_suggs and word in spell_suggs:
        spell_suggs.remove(word)

    if spell_suggs:
        suggs = suggs + spell_suggs
        confs = confs + [1 / (n + 2) for n in range(len(spell_suggs))]

    if not spell_is_correct and not spell_suggs:
        suggs = [word]
        confs = [0.1]

    if flag_corrected:
        suggs = flag_words_if_different(suggs, word)

    if return_confidences:
        return suggs[:max_suggestions], confs[:max_suggestions]
    else:
        return suggs[:max_suggestions]


# AUXILIARY FUNCTIONS #
# hunspell-spellchecker
dir_path = os.path.dirname(os.path.realpath(__file__))
hunspell_folder = os.path.join(dir_path, '..', 'data', 'hunspell')
spellchecker = hunspell.HunSpell(os.path.join(hunspell_folder, 'de_DE.dic'),
                                 os.path.join(hunspell_folder, 'de_DE.aff'))

from nltk import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer
detokenizer = MosesDetokenizer()
def words_detokenize(words):
    return detokenizer.detokenize(words, return_str=True)


def flag_words_if_different(words, reference_word):
    """
    Take a list of `words` and a  `reference_word`.a
    Return new list where words which differ from `reference_word` are flagged
    (surrounded by asterisk).

    Example:
    flag_words_if_different(["Ei", "Eis"], "Ei") returns ["Ei", "*Eis*"].
    """
    return [('*' + word + '*') if (word != reference_word) else word
            for word in words]

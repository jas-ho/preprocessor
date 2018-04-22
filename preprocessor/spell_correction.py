import hunspell
import editdistance
import os


# MAIN FUNCTION #
def spell_correct_word(word, flag_corrected=False, return_confidences=False):
    """
    Take `word` and return a list of spell-corrected versions of `word`.
    If `word` is correctly spelled, return [`word`].

    If `return_confidences` is True (default: False):
        Return list of confidences (floats between zero and 1) as second output.

    If `flag_corrected` is True (default: False):
        Surround corrected words  with '*'.
        ("corrected words" are suggested words which are not equal to input word)
    """
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
        return suggs, confs
    else:
        return suggs


# AUXILIARY FUNCTIONS #
dir_path = os.path.dirname(os.path.realpath(__file__))
hunspell_folder = os.path.join(dir_path, '..', 'data', 'hunspell')
spellchecker = hunspell.HunSpell(os.path.join(hunspell_folder, 'de_DE.dic'),
                                 os.path.join(hunspell_folder, 'de_DE.aff'))


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


# CURRENTLY UNUSED #
def get_confidence(sugg, pos, word):
    """
    Return confidence (:float) in suggested correction `sugg` for `word`
    based on
    - Levenshtein edit distance between `sugg` and `word`
    - position `pos` at which `sugg` appears in list of hunspell-suggestions
    """
    conf_edit_dist = normed_inv_edit_dist(sugg, word)
    conf_hunspell_order = 1 / (pos + 1)
    return conf_edit_dist * conf_hunspell_order


def normed_inv_edit_dist(word1, word2):
    """
    Return 1/(1 + dist(word1, word2)).
    dist(word1, word2): Levenshtein edit distance between `word1` and `word2`.
    """
    return 1 / (1 + editdistance.eval(word1, word2))

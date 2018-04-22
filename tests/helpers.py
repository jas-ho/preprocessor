import random
import string

def misspell_word(word):
    """
    Return misspelled version of `word`.
    Misspelling is randomly chosen to be one of
    - character deletion
    - character insertion
    - character transposition
    Preserves the case of the word.
    """
    misspell = random.choice(
        [rand_delete_char,
         rand_insert_char,
         rand_transpose_chars])
    return misspell(word)


def rand_delete_char(word):
    """Return `word` but with one randomly chosen character deleted."""
    rand_pos = random.randint(0, len(word)-1)
    return word[:rand_pos]+word[rand_pos+1:]


def rand_insert_char(word):
    """Return `word` but with one randomly chosen character inserted."""
    rand_pos = random.randint(0, len(word)-1)
    rand_char = random.choice(string.ascii_lowercase)
    mis_word = word[:rand_pos]+rand_char+word[rand_pos:]
    if word.istitle():
        return mis_word.title()
    else:
        return mis_word


def rand_transpose_chars(word):
    """Return `word` but with two randomly chosen neighboring characters transposed."""
    rand_pos = random.randint(1, len(word)-1)
    word1, word2 = word[:rand_pos], word[rand_pos:]
    mis_word = word1[:-1]+word2[0]+word1[-1]+word2[1:]
    if word.istitle():
        return mis_word.title()
    else:
        return mis_word

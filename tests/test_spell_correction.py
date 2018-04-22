from .context import spell_correct_word, spell_correct_text
import pytest
from hypothesis import given
from hypothesis import strategies as st
import numpy


# UNIT TESTS: spell_correct_word #
# parametrized tests via hypothesis
allowed_chars = st.characters(
    max_codepoint=200, whitelist_categories=('Lu', 'Ll'))


@given(st.text(allowed_chars, min_size=1))
@pytest.mark.spell_correct_word
def test__spell_correct_word__return_type(word):
    # suggestions is a list of strings
    suggestions = spell_correct_word(word)
    assert type(suggestions) is list
    assert set(map(type, suggestions)) == {str}

    # confidences is a list of floats
    suggestions, confidences = spell_correct_word(
        word, return_confidences=True)
    assert len(suggestions) == len(confidences)
    assert type(suggestions) is list
    assert type(confidences) is list
    assert set(map(type, suggestions)) == {str}
    assert set(map(type, confidences)) == {float}


# explicit tests
@pytest.mark.spell_correct_word
def test__spell_correct_word__correct_input():
    correct_word = 'Ei'
    suggs, confs = spell_correct_word(correct_word, return_confidences=True)
    assert suggs[0] == correct_word, \
        "First suggestion should be input word if input word is correct."
    assert confs[0] == 1., \
        "Confidence in a correct input word should be 1."


@pytest.mark.spell_correct_word
def test__spell_correct_word__flag_corrected():
    suggs = spell_correct_word('Abtt', flag_corrected=True)
    suggs[:2] == ['*Abt*', '*Abtat*']


@pytest.mark.spell_correct_word
def test__spell_correct_word__unrecognized_input():
    unknown_word = 'Donaudampschifffahrtskapitänsmützenstofffabrik'
    sugg, conf = spell_correct_word(unknown_word, return_confidences=True)
    assert conf == [0.1], \
        """Unrecognized word for which no suggestions are found:
            Confidence should be 0.1."""
    assert sugg == [unknown_word], \
        """Unrecognized word for which no suggestions are found:
        Unrecognized word should be returned as sole suggestion."""


@pytest.mark.spell_correct_word
def test__spell_correct_word__confidences():
    __, confs = spell_correct_word('Tset', return_confidences=True)
    assert confs == [1 / 2, 1 / 3, 1 / 4, 1 / 5]


# UNIT TESTS: spell_correct_text #
# parametrized tests via hypothesis
allowed_chars = st.characters(
    max_codepoint=200, whitelist_categories=('Lu', 'Ll'))


@given(st.text(allowed_chars, min_size=1))
@pytest.mark.spell_correct_text
def test__spell_correct_text__return_type(word):
    # suggestions is a list of strings
    # confidences is a list of floats
    suggestions, confidences = spell_correct_text(word)
    assert len(suggestions) == len(confidences)
    assert type(suggestions) is list
    assert type(confidences) is list
    assert set(map(type, suggestions)) == {str}
    assert set(map(type, confidences)) == {numpy.float64}


# explicit tests
@pytest.mark.spell_correct_text
def test__spell_correct_text__correct_input():
    correct_sent = 'A'
    suggs, confs = spell_correct_text(correct_sent)
    assert suggs[0] == correct_sent, \
        "First suggestion should be input text if input text is correct."
    assert confs[0] == 1., \
        "Confidence in a correct input text should be 1."


@pytest.mark.spell_correct_text
def test__spell_correct_text__unknown_input():
    unknown_word = 'Donaudampschifffahrtskapitänsmützenstofffabrik'
    unknown_text = unknown_word + " " + unknown_word + "."
    sugg, conf = spell_correct_text(unknown_text)
    assert conf == [0.1 * 0.1], \
        """Unrecognized text for which no suggestions are found:
            Confidence should be 0.1**(no of words)."""
    assert sugg == [unknown_text], \
        """Unrecognized text for which no suggestions are found:
        Unrecognized text should be returned as sole suggestion."""

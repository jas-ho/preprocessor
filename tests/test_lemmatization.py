from .context import test_dir, spell_correct, \
                     pos_tag_sentence, pos_tag, \
                     lemmatize, lemmatize_sentence
import pytest
from hypothesis import given
from hypothesis import strategies as st
import os
import json


# UNIT TESTS: pos_tag_sentence #
# parametrized tests via hypothesis
allowed_chars = st.characters(
    max_codepoint=200, whitelist_categories=('Lu', 'Ll'))


@given(st.text(allowed_chars, min_size=1))
@pytest.mark.lemmatize_sentence
def test__lemmatize_sentence__return_type(sent):
    postagged = pos_tag_sentence(sent)
    lemmatized = lemmatize_sentence(postagged)
    assert type(lemmatized) is list
    assert type(lemmatized[0]) is tuple
    assert len(lemmatized[0]) == 2
    assert type(lemmatized[0][0]) is str
    assert type(lemmatized[0][1]) is str

# explicit tests
@pytest.mark.lemmatize_sentence
def test__lemmatize_sentence__explicit():
    sent_in = "Ein Mann."
    postagged_sent = pos_tag_sentence(sent_in)
    lemmatized = lemmatize_sentence(postagged_sent)
    assert lemmatized == [('Ein', 'ein'), ('Mann', 'Mann'), ('.', '--')]


# INTEGRATION TESTS: lemmatize #
@pytest.mark.current
@pytest.mark.lemmatize
def test__spell_correct__json_input():
    in_file = os.path.join(test_dir, 'data',
                           'challenge_json_input_format.json')
    out_file = os.path.join(test_dir, 'data',
                            'challenge_output_lemmatizer.json')

    json_spell_corrected = spell_correct(in_file)
    json_pos_tagged = pos_tag(json_spell_corrected)
    json_lemmatized = lemmatize(json_spell_corrected,
                                output_file=out_file)

    json_in = json.load(open(in_file))
    for sent in json_in["input"]:
        assert sent in json_lemmatized, \
            "Every input sentence should be a key in the output structure."

    # consider a simple example...
    sent = "Ein Ei und noch ein Ei."
    suggestions = json_lemmatized[sent]["spellingcorrections"]
    best_sugg = suggestions[0]
    assert sent in best_sugg, 'First suggestion should be input if input is correct'

    assert best_sugg[sent]["lemmatization"] == [{'Ein': 'ein'},
                                            {'Ei': 'Ei'},
                                            {'und': 'und'},
                                            {'noch': 'noch'},
                                            {'ein': 'ein'},
                                            {'Ei': 'Ei'},
                                            {'.': '--'}]

from .context import test_dir, spell_correct, pos_tag_sentence, pos_tag
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
@pytest.mark.pos_tag_sentence
def test__pos_tag_sentence__return_type(sent):
    tagged = pos_tag_sentence(sent)
    assert type(tagged) is list
    assert type(tagged[0]) is tuple
    assert len(tagged[0]) == 2
    assert type(tagged[0][0]) is str
    assert type(tagged[0][1]) is str

# explicit tests
@pytest.mark.pos_tag_sentence
def test__pos_tag_sentence__explicit():
    sent_in = "Ein Mann."
    tagged = pos_tag_sentence(sent_in)
    assert tagged == [('Ein', 'ART'), ('Mann', 'NN'), ('.', '$.')]


# INTEGRATION TESTS: pos_tag #
@pytest.mark.pos_tag
def test__spell_correct__json_input():
    json_in = os.path.join(test_dir, 'data',
                           'challenge_json_input_format.json')
    json_out = os.path.join(test_dir, 'data',
                            'challenge_output_postagger.json')

    json_spell_corrected = spell_correct(json_in)

    json_pos_tagged = pos_tag(json_spell_corrected, output_file=json_out)

    json_in = json.load(open(json_in))
    for sent in json_in["input"]:
        assert sent in json_pos_tagged, \
            "Every input sentence should be a key in the output structure."

        suggestions = json_pos_tagged[sent]["spellingcorrections"]

        for sugg_dict in suggestions:
            sugg = list(sugg_dict.keys())[0]
            postags = sugg_dict[sugg]["postagger"]

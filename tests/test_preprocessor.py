from .context import test_dir, preprocess
import pytest
from hypothesis import given
from hypothesis import strategies as st
import os
import json


# INTEGRATION TESTS: preprocess #
@pytest.mark.preprocess
def test__spell_correct__json_input():
    path_in = os.path.join(test_dir, 'data',
                           'challenge_json_input_format.json')
    json_in = json.load(open(path_in))

    path_out = os.path.join(test_dir, 'data',
                            'challenge_output_preprocessor.json')
    json_out = preprocess(path_in, output_file=path_out)

    for sent in json_in["input"]:
        assert sent in json_out, \
            "Every input sentence should be a key in the output structure."

        suggestions = json_out[sent]["spellingcorrections"]

        for sugg_dict in suggestions:
            sugg = list(sugg_dict.keys())[0]
            postags = sugg_dict[sugg]["postagger"]

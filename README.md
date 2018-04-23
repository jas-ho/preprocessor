# preprocessor

This python repository contains tools for a simple preprocessing pipeline for NLP for the German language.
It implements the following main functions
- `spell_correct`: a wrapper for the hunspell-spellchecker
- `pos_tag`: a pos-tagger trained with data from the TIGER corpus
- STILL MISSING: `lemmatize`: a lemmatizer based on (amongst others)
-- lookup from the tiger corpus,
-- lemmatization via the pattern.de module

The full end-to-end pipeline is provided by the function `preprocess`.

## Getting Started
All the main functions (`spell_correct`, `pos_tag`, `lemmatize`, `preprocess`) are found in separate file in the sub-folder ./preprocessor.

They can be imported in your python-code as follows:
```
from preprocessor import preprocess, spell_correct, pos_tag, lemmatize
```

Alternatively, the script preprocess_german_json.py in the top-level directory can be invoked as follows
```
python preprocess_german_json.py input.json output.json
```
This will take the file input.json, apply the preprocessing to the sentences in input.json, and store the result in output.json.

Note that input.json is expected to be in the following format:
    - a single key: "input"
    - corresponding value: list of German input sentences s1, s2,... :str.



### Prerequisites

The python packages which are explicitly imported and their versions are listed in requirements.txt


## Running the tests

Tests are stored in the sub-folder ./tests. They can be run using pytest as follows:
```
cd tests && pytest
```

## References
- http://www.nltk.org/book/ch06.html as general introduction
- https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/ for how to use the python-wrapper for hunspell
- https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/ for how to train a POS-tagger using the TIGER corpus  (relying on the German tagger classifier from Philipp Nolte)
- https://datascience.blog.wzb.eu/2017/05/19/lemmatization-of-german-language-text/ for how to implement improved lemmatization (a reference implementation was provided here: https://github.com/WZBSocialScienceCenter/germalemma)

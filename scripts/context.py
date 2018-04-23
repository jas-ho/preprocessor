import sys
import os

script_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(script_dir, '..'))
module_dir = os.path.abspath(os.path.join(module_dir, '3rd_party/'))
sys.path.insert(0, module_dir)

from ClassifierBasedGermanTagger import ClassifierBasedGermanTagger

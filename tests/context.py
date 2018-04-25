import sys
import os

test_dir = os.path.abspath(os.path.dirname(__file__))
module_dir = os.path.abspath(os.path.join(test_dir, '..'))
sys.path.insert(0, module_dir)

from preprocessor import *

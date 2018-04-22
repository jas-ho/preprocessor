import sys
import os

test_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(test_dir, '..'))
sys.path.insert(0, parent_dir)

from preprocessor import *

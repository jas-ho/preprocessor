# simple script to keep an eye on the execution time
#  of the different preprocessing steps
#
#  for now: only "spell_correct_text"

from preprocessor import spell_correct_text
from datetime import datetime

print("""
Measuring runtime
of "spell_correct_text"
on input "Das ist ein einfacher Test."...""")
tic = datetime.now()
corr = spell_correct_text('Das ist ein einfacher Test.')
toc = datetime.now()
print('Elapsed time: {} sec'.format(
    (toc - tic).total_seconds()))

# combine one or many entries in victim.dat to guess password

import itertools
entries = [line.rstrip() for line in open('victim.dat', 'r')]
print(entries)
combinations = itertools.combinations(entries, 2)
combinations = list(combinations)
import pdb
pdb.set_trace()
# print(combinations)
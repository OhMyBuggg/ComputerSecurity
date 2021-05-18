# combine one or many entries in victim.dat to guess password

import itertools
entries = [line.rstrip() for line in open('victim.dat', 'r')]
print(entries)
combinations = itertools.combinations(entries, 3)
combinations = list(combinations)
print(combinations)
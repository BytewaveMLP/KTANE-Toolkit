#!/usr/bin/env python3

import itertools

passwords = set(itertools.chain.from_iterable(
i.split('\t') for i in '''
about	after	again	below	could
every	first	found	great	house
large	learn	never	other	place
plant	point	right	small	sound
spell	still	study	their	there
these	thing	think	three	water
where	which	world	would	write
'''.strip().splitlines()))

print('''
KTANE Toolkit - Passwords solver

Enter the possible values for each letter from left to right.
''')

index = 1
while True:
	letters = set(input('Letter {}: '.format(index)))
	passwords = {i for i in passwords if i[index] in letters}
	print(*passwords)
	index += 1
	if index > 5 or len(passwords) < 2:
		break


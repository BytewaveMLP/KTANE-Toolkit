#!/usr/bin/env python3

print('''
KTANE Toolkit - Wire sequences solver

Inputs should be in order on the left side from top to bottom.
Press ctrl+C to exit.

Input format:
  [Color][Rightside position]
Color format:
  (1) Red   (2) Blue  (3) Black
Example:
  1b 2c 2b
''')

cuts = {
	'1': 'C B A AC B AC ABC AB B'.split(' ')[::-1],
	'2': 'B AC B A B BC C AC A'.split(' ')[::-1],
	'3': 'ABC AC B AC B BC AB C C'.split(' ')[::-1],
}

while True:
	print(*(
		'Cut' if position in cuts[color].pop() else '---'
		for color, position in input('Wires: ').strip().upper().split(' ')
	), '\n')


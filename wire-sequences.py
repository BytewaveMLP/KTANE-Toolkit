#!/usr/bin/env python3

print('''
KTANE Toolkit - Wire sequences solver

Inputs should be in order on the left side from top to bottom.
Press ctrl+C to exit.

Input format:
  [Color][Rightside position]
Color format:
  (1/R) Red
  (2/B) Blue
  (3/K) Black
Example:
  RB RC kc 1a
''')

cuts = {
	'R': 'C B A AC B AC ABC AB B'.split(' ')[::-1],
	'B': 'B AC B A B BC C AC A'.split(' ')[::-1],
	'K': 'ABC AC B AC B BC AB C C'.split(' ')[::-1],
}
cuts['1'], cuts['2'], cuts['3'] = cuts['R'], cuts['B'], cuts['K']

while True:
	print(*(
		'Cut' if position in cuts[color].pop() else '---'
		for color, position in input('Wires: ').strip().upper().split(' ')
	), '\n')

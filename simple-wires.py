#!/usr/bin/env python3

import sys

print("""
KTANE Toolkit - Simple wires solver

Wire input format: BYRWK
Wire format:       K
(K)Black (B)lue (Y)ellow (R)ed (W)hite
""")

wires = list(input('Wire sequence: ').upper())
serial_last_odd = int(input('Last digit of serial: ')) % 2 == 1

black_count = wires.count('K')
blue_count = wires.count('B')
yellow_count = wires.count('Y')
red_count = wires.count('R')
white_count = wires.count('W')
last_wire = wires[-1]

to_cut = 0

if len(wires) == 3:
	if 'R' not in wires:
		to_cut = 2
	elif last_wire == 'W':
		to_cut = 3
	elif blue_count > 1:
		to_cut = wires.rfind('B') + 1
	else:
		to_cut = 3
elif len(wires) == 4:
	if red_count and serial_last_odd:
		to_cut = wires.rfind('R') + 1
	elif last_wire == 'Y' and red_count == 0:
		to_cut = 1
	elif blue_count == 1:
		to_cut = 1
	elif yellow_count > 1:
		to_cut = 5
	else:
		to_cut = 2
elif len(wires) == 5:
	if last_wire == 'K' and serial_last_odd:
		to_cut = 4
	elif red_count == 1 and yellow_count > 1:
		to_cut = 1
	elif black_count:
		to_cut = 2
	else:
		to_cut = 1
elif len(wires) == 6:
	if yellow_count == 0 and serial_last_odd:
		to_cut = 3
	elif yellow_count == 1 and white_count > 1:
		to_cut = 4
	elif red_count == 0:
		to_cut = 6
	else:
		to_cut = 4
else:
	print('ERROR: Invalid number of wires specified (expected 3-6, got ' + str(len(wires)) + ')', file=sys.stderr)
	sys.exit(1)

print('CUT: ' + str(to_cut))

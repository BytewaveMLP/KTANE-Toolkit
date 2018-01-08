#!/usr/bin/env python3

print("""
KTANE Toolkit - Complex wires solver

NOTE: White striped colored wires are the same as solid wires

Wire input format: Wire1|Wire2|Wire3
Wire format:       RBLS
	(R)ed (B)lue (L)ight (S)tar
	If flag isn't needed, exclude it
	Empty wires should be left empty (space)
Example: RB|BLS|R||S
""")

def wire_action(flags):
	return 'CDCBSPDPSBCSSBPD'[sum(1 << 'LSBR'.index(f) for f in flags)]

def should_cut(wire, serial, parallel, batteries):
	action = wire_action(wire)

	if action == 'D':
		return False
	if action == 'S' and not serial:
		return False
	if action == 'P' and not parallel:
		return False
	if action == 'B' and not batteries:
		return False

	return True

serial_last_even = int(input('Last digit of serial: ')) % 2 == 0
has_parallel = input('Has parallel port? (Y/N): ').lower() == 'y'
has_two_or_more_batteries = int(input('Number of batteries?: ')) > 2
wires = input('Wire readout: ').upper().split('|')

for i in range(0, len(wires)):
	cut = should_cut(wires[i], serial_last_even, has_parallel, has_two_or_more_batteries)
	print(str(i + 1) + ': ' + ('CUT' if cut else '---'))

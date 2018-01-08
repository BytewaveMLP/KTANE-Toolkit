#!/usr/bin/env python 3

import operator
import collections
import itertools
import functools
import numbers
import heapq

# (x -> y -> z) -> (y -> x -> z)
def flip(func):
	def inner(*args, **kwargs):
		return func(*(args[::-1]), **kwargs)
	return inner

# (x -> y -> z) -> (Vector x -> a -> Vector z)
def vector_operator(op):
	@functools.singledispatch
	def func(other, self):
		return Vector(map(op, self, other))
	@func.register(numbers.Number)
	def _(other, self):
		return Vector(map(op, self, itertools.repeat(other)))
	return flip(func)

# Vector a :: [a, a]
class Vector(list):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def __str__(self):
		return '<{}>'.format(','.join(map(str, self)))
	def __hash__(self):
		return hash(tuple(self))
	__add__ = vector_operator(operator.add)
	__sub__ = vector_operator(operator.sub)
	__mul__ = vector_operator(operator.mul)
	__floordiv__ = vector_operator(operator.floordiv)
	__truediv__  = vector_operator(operator.truediv)

# Direction :: char
# Position  :: Vector Int
# direction :: Direction -> Position
directions = {
	'^' : Vector([ 0,-1]),
	'v' : Vector([ 0, 1]),
	'<' : Vector([-1, 0]),
	'>' : Vector([ 1, 0]),
}
mirrors = {
	'^' : 'v',
	'v' : '^',
	'<' : '>',
	'>' : '<',
}

mazes = '''
#############
#     #     #
# ### # #####
#O#   #     #
# # ####### #
# #   #    O#
# ### # ### #
# #     #   #
# ######### #
#     #   # #
# ### # ### #
#   #   #   #
#############
#############
#     #     #
### ### # ###
#   #   #O  #
# ### ##### #
# #   #     #
# # ### ### #
#  O#   # # #
# ### ### # #
# # # #   # #
# # # # ### #
# #   #     #
#############
#############
#     # #   #
# ### # # # #
# # # #   # #
### # ##### #
#   # #   # #
# # # # # # #
# # # #O# #O#
# # # # # # #
# #   # # # #
# ##### # # #
#       #   #
#############
#############
#O  #       #
# # ####### #
# # #       #
# # # ##### #
# #   #   # #
# ##### #####
#O#         #
# ######### #
#         # #
# ####### # #
#     #   # #
#############
#############
#           #
######### # #
#         # #
# ##### #####
#   #   #O  #
# # ##### # #
# #     # # #
# ##### ### #
# #       # #
# # ####### #
# #    O    #
#############
#############
# #   #  O  #
# # # ### # #
# # # #   # #
# # # # ### #
#   # # #   #
# ##### # ###
#   #   # # #
### # # # # #
#   #O# #   #
# ##### ### #
#       #   #
#############
#############
#  O    #   #
# ##### # # #
# #   #   # #
# # ####### #
#   #   #   #
##### ### ###
#   #     # #
# # # ##### #
# # #     # #
# ####### # #
#  O        #
#############
#############
# #    O#   #
# # ### # # #
#     #   # #
# ######### #
# #       # #
# # ##### # #
# #  O#     #
# ### #######
# # #       #
# # #########
#           #
#############
#############
# #         #
# # ##### # #
# # #O  # # #
# # # ### # #
#     #   # #
# ##### ### #
# # #   #   #
# # # ##### #
#O# # #   # #
# # # # # ###
#   #   #   #
#############
'''.strip('\n').splitlines()

# [[a]] -> Position -> bool
def bounded(grid, pos):
	x, y = pos
	return 0 <= y < len(grid) and 0 <= x < len(grid[y])

# [[a]] -> Position -> a
def access(grid, pos):
	x, y = pos
	return grid[y][x]

# Position -> Position
def preposition(pos):
	return (pos + 1) // 2

# [[char]] -> ({Position : {Direction}}, {Position})
def preprocess(maze):
	queue = collections.deque([Vector([1, 1])])
	edges = collections.defaultdict(set)
	indicators = set()
	while queue:
		position = queue.popleft()
		if access(maze, position) == 'O':
			indicators.add(position)
		for direction, vector in directions.items():
			newpos1 = position + vector
			newpos2 = newpos1  + vector
			if bounded(maze, newpos2) and access(maze, newpos1) != '#':
				edges[position].add(direction)
				if newpos2 not in edges:
					queue.append(newpos2)
	return (
		{((k+1)//2):v for k,v in edges.items()},
		{(i+1)//2 for i in indicators}
	)

mazes = list(map(preprocess, zip(*([iter(mazes)]*13))))

# indicators :: {Position : set}
indicators = collections.defaultdict(set)
for n, (_, indic) in enumerate(mazes):
	for i in indic: indicators[i].add(n)
mazes = [edge for edge, _ in mazes]

# {Position : {Direction}} -> Position
#   -> ({Position : int}, {Position : Direction})
def dijkstra(edges, start):
	queue = [(0, start)]
	step = collections.defaultdict(lambda: None)
	dist = collections.defaultdict(lambda: float('inf'))
	dist[start] = 0
	while queue:
		w, p = heapq.heappop(queue)
		w += 1
		for d in edges[p]:
			p1 = p + directions[d]
			if p1 not in edges:
				continue
			if w < dist[p1]:
				dist[p1] = w
				step[p1] = d
				heapq.heappush(queue, (w, p1))
	return dict(dist), dict(step)

# IO int
def _input(*args, **kwargs):
	n = None
	while n is None:
		try:
			n = int(input(*args, **kwargs))
			if not (0 <= n < 6): n = None
		except ValueError:
			pass
	return n




print('Note: grids in this script are 1-indexed')

maze = set(range(len(mazes)))
while True:
	x = int(_input('Indicator X: '))
	y = int(_input('Indicator Y: '))
	p = Vector([x, y])
	maze &= indicators[p]
	if len(maze) == 0:
		print('No maze found, trying again')
		maze = set(range(len(mazes)))
	elif len(maze) == 1:
		print('Maze found')
		maze = mazes[list(maze)[0]]
		break
	else:
		print('More than 1 suitable maze, enter other indicator')

x = int(_input('Current X: '))
y = int(_input('Current Y: '))
current = Vector([x, y])

x = int(_input('Target X: '))
y = int(_input('Target Y: '))
target = Vector([x, y])

_, step = dijkstra(maze, current)
steps = []
while target != current:
	s = step[target]
	steps.append(s)
	target = target + directions[mirrors[s]]
steps = steps[::-1]

print(*steps)
print(*('{}{}'.format(len(list(g)), k) for k, g in itertools.groupby(steps)))


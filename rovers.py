from collections import Counter
"""
Assumptions:
- The plateau is rectangular and so rovers will not move past the edge
- Each block is big enough to have more than 1 Rover within the same block, with no collisions, However rovers cooridinates is being stored.
- Input is terminated by a blank line
"""

class Orientation:
	def __init__(self, value, delta):
		self.value = value
		self.delta = delta
		self.left = None
		self.right = None


class Compass:
	def __init__(self, starting_orientation):
		# Compass is a doubly linked list 
		north = Orientation('N', (0,1))
		east  = Orientation('E', (1,0))
		south = Orientation('S', (0,-1))
		west  = Orientation('W', (-1,0))

		north.right = east
		east.right  = south
		south.right = west
		west.right  = north

		north.left = west
		west.left  = south
		south.left = east
		east.left  = north

		lookup = {'N':north, 'E':east, 'S':south, 'W':west}
		self.current_orientation = lookup[starting_orientation]

	def rotate(self, direction):
		if direction != 'L' and direction != 'R':
			return

		if direction == 'L':
			self.current_orientation = self.current_orientation.left
		else:
			self.current_orientation = self.current_orientation.right


def check_move_validity(coordinates, rovers_locations, n_rows, n_columns):
	if coordinates[1] > n_rows or coordinates[1] < 0:
		return False
	if coordinates[0] > n_columns or coordinates[0] < 0:
		return False
	if rovers_locations[coordinates] > 0:
		print("Warning: another rover is in the block")

	return True


def move_rovers(rovers, rovers_locations, n_rows, n_columns):
	final_rovers = []
	for rover in rovers:
		[r_s_x, r_s_y], current_compass, rover_instructions = rover
		rovers_locations[(r_s_x, r_s_y)] -= 1

		for instruction in rover_instructions:
			if instruction == 'M':
				delta = current_compass.current_orientation.delta
				future_coordinates = (r_s_x + delta[0], r_s_y + delta[1])
				# print("Delta", delta, "future", future_coordinates)
				if check_move_validity(future_coordinates, rovers_locations, n_rows, n_columns):
					r_s_x, r_s_y = future_coordinates
				else:
					print("unsafe move")

			current_compass.rotate(instruction)

		rovers_locations[(r_s_x, r_s_y)] += 1
		# print(r_s_x, r_s_y, current_compass.current_orientation.value)	
		final_rovers.append([r_s_x, r_s_y, current_compass.current_orientation.value])
	return final_rovers




# Complexity Time: O(R*I) where R is number of rovs, I instruction length
#			 Space: O(R)


n_columns, n_rows = [int(n) for n in input().split()]
# to keep track of rovers locations
rovers_locations = Counter()
rovers = []

while True:
	invalid_initials = False
	rover_initials = input()
	if rover_initials == '':
		break
	# rover start x, rover start y, rover start orientation
	r_s_x, r_s_y = [int(n) for n in rover_initials.split()[:-1]]
	if r_s_x < 0 or r_s_x > n_columns or \
		r_s_y < 0 or r_s_y > n_rows:
		print("invalid starting pos, ignoring")
		invalid_initials = True


	r_s_o = rover_initials.split()[-1]
	if r_s_o not in "NESW":
		print("invalid starting orientation ignoring rov")
		invalid_initials = True

	rover_instructions = input()

	if invalid_initials:
		continue

	rovers_locations[(r_s_x, r_s_y)] += 1
	rovers.append([[r_s_x, r_s_y], Compass(r_s_o), rover_instructions])

print(*move_rovers(rovers, rovers_locations, n_rows, n_columns), sep='\n')


# ================================ TESTS =========================================
import random
import string
random.seed("seed")

print("Testing Compass")
print("it should initialise correctly to the right orientation")
for o in 'NESW':
	compass = Compass(o)
	assert compass.current_orientation.value == o


print("it should complete a R cycle perserving the right order")
compass = Compass('N')
for o in 'NESW':
	assert o == compass.current_orientation.value
	compass.rotate('R')

print("it should complete a L cycle perserving the right order")
compass = Compass('N')
for o in 'NWSE':
	assert o == compass.current_orientation.value
	compass.rotate('L')

print("it should ignore any input other than R and L")
compass = Compass('N')
for i in range(10):
	compass.rotate(random.choice(string.ascii_letters))
	assert compass.current_orientation.value == 'N'


print("Testing Rovers")
print("Test moving up vertically and back down")
rov = [[[0,0], Compass('N'), 'MM']]
final = move_rovers(rov, Counter(), 2, 0)
assert final[0][:2] == [0,2]
rov = [[[0,0], Compass('N'), 'MMLLMM']]
final = move_rovers(rov, Counter(), 2, 0)
assert final[0][:2] == [0,0]

print("Test moving horizontally and back")
rov = [[[0,0], Compass('E'), 'MM']]
final = move_rovers(rov, Counter(), 0, 2)
assert final[0][:2] == [2,0]
rov = [[[0,0], Compass('E'), 'MMLLMM']]
final = move_rovers(rov, Counter(), 0, 2)
assert final[0][:2] == [0,0]


print("Test moving in any direction straight and reverting should lead to the starting point")
rov = [[[3,3], Compass(random.choice('NESW')), 'MMLLMM' if random.random() > 0.5 else 'MMRRMM']]
final = move_rovers(rov, Counter(), 5,5)
assert final[0][:2] == [3,3]

print("Test rotating cycles should have no effect")
rov1 = [[[3,3], Compass('N'), 'L'*65 + 'M' + 'R'*65 + 'M']]
rov2 = [[[3,3], Compass('N'), 'LMRM']]
assert move_rovers(rov1, Counter(), 5,5) == move_rovers(rov2, Counter(), 5, 5 )


print('it must prevent rovs from running across the edge')
rov = [[[0,0], Compass('N'), 'MMM']]
final = move_rovers(rov, Counter(), 2, 0)
assert final[0][:2] == [0,2]
rov = [[[0,0], Compass('E'), 'MMM']]
final = move_rovers(rov, Counter(), 0, 2)
assert final[0][:2] == [2,0]

#===================================================================

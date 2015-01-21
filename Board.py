import random

class Board(object):
	def __init__(self, size, n_types):
		super(Board, self).__init__()
		self.size = size
		self.n_types = n_types
		self.board = [[0] * size[1]] * size[0]

	def randomize(self):
		self.board = [[random.randint(1, self.n_types) for i in 
			xrange(self.size[1])] for j in xrange(self.size[0])]

	def check_for_pairs(self):
		# Returns pair-coordinates of adjacent colors and their direction (row/col).
		self.hor = []
		self.ver = []
		#checks to the right
		for i in range(self.size[0]):
			for j in range(self.size[1]-1):
				if self.board[i][j] == self.board[i][j+1]:
					# Get color of matching pair later.
					
					self.hor.append([i,j, 'color'])
		
		print self.hor

		#checks below
		for i in range(self.size[0]-1):
			for j in range(self.size[1]):
				if self.board[i][j] == self.board[i+1][j]:
					# Get color of matching pair later.
					
					self.ver.append([i, j, 'color'])

		print self.ver

	def remove(self, i, j):
		# don't call collapse! remove will be called >= 3 times before
		# collapse is called.
		if i >= self.size[0] or j >= self.size[1]:
			raise ValueError("Attempt to remove piece outside of \
			                 board bounds")
		for row in xrange(i, 0, -1):
			self.board[row][j] = self.board[row-1][j]
		self.board[0][j] = 0

	def is_in_run(self, i, j):
		# Check to the left, right, up, and down, then use a list comp
		# to create a list of points to remove. This handles the
		# creation of multiple runs in one move.
		
		run = True
		for offset in xrange(1, 3): # Check down
			if i + offset >= self.size[0]: # don't go out of bounds
				run = False
				break
			if self.board[i][j] != self.board[i + offset][j]:
				run = False
				break
		if run:
			return True
		
		run = True
		for offset in xrange(1, 3): # Check up
			if i - offset < 0:
				run = False
				break
			if self.board[i][j] != self.board[i - offset][j]:
				run = False
				break
		if run:
			return True

		run = True
		for offset in xrange(1, 3): # Check right
			if j + offset >= self.size[1]:
				run = False
				break
			if self.board[i][j] != self.board[i][j + offset]:
				run = False
				break
		if run:
			return True

		run = True
		for offset in xrange(1, 3): # Check left
			if j - offset < 0:
				run = False
				break
			if self.board[i][j] != self.board[i][j - offset]:
				run = False
				break
		if run:
			return True

		return False


	def collapse(self):
		# Return false if no possible runs to collapse.
		run_points = [(i, j) for i in xrange(self.size[0]) for j in 
			xrange(self.size[1]) if self.is_in_run(i, j)]
		if len(run_points) == 0:
			return False
		for point in run_points:
			self.remove(point[0], point[1])
		return True

	def move(self, a, b):
		if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
			raise ValueError("Invalid targets for move.")
		self.board[a[0]][a[1]], self.board[b[0]][b[1]] = \
			self.board[b[0]][b[1]], self.board[a[0]][a[1]]
		
		# DISABLED FOR DEBUG
		# if self.collapse() is False:
		# 	raise ValueError("Move does not create any runs.")


if __name__ == '__main__':
	random.seed()
	board = Board((3, 3), 5)
	board.board = [[1, 2, 1], [2, 1, 1], [1, 2, 2]]
	print board.collapse()
	board.move((0, 1), (1, 1))
	print board.collapse()
	print board.grid_display()
	# Why is 1 still at (0, 1)?

	board.check_for_pairs()

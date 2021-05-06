from copy import deepcopy

def removeMinusOne(x):
	if x == ' -1 ':
		return '   '
	return x

class sudokuState:

	def __init__(self, m, r, c):
		self.m = deepcopy(m)
		self.r = r
		self.c = c

	def rowOk(self):
		for i in range(0, 9):
			visited = set()
			for j in range(0, 9):
				if self.m[i][j] != -1:
					if self.m[i][j] in visited:
						return False
					visited.add(self.m[i][j])
		return True

	def colOk(self):
		for j in range(0, 9):
			visited = set()
			for i in range(0, 9):
				if self.m[i][j] != -1:
					if self.m[i][j] in visited:
						return False
					visited.add(self.m[i][j])
		return True

	def boxOk(self):
		X = {
				0: [0, 1, 2],
				1: [3, 4, 5],
				2: [6, 7, 8]
		}
		Y = {
				0: [0, 1, 2],
				1: [3, 4, 5],
				2: [6, 7, 8]
		}
		for boxR in range(0, 3):
			for boxC in range(0, 3):
				visited = set()
				for i in X[boxR]:
					for j in Y[boxC]:
						if self.m[i][j] != -1:
							if self.m[i][j] in visited:
								return False
							visited.add(self.m[i][j])
		return True

	def isValid(self):
		if self.rowOk() and self.colOk() and self.boxOk():
			return True
		return False

	def isWin(self):
		for i in range(0, 9):
			for j in range(0, 9):
				if self.m[i][j] == -1:
					return False
		return self.isValid()

	def next(self):
		if self.c != 8:
			return self.r, self.c + 1
		return self.r + 1, 0

	def __str__(self):
		return '\n-----------------------------------\n'.join(['|'.join(map(removeMinusOne, [' ' + str(cell) + ' ' for cell in row])) for row in self.m])

if __name__ == '__main__':

	# Enter the starting state
	start = [
				[-1,3,-1,9,-1,-1,1,-1,-1],
				[-1,-1,9,-1,-1,5,-1,7,-1],
				[6,-1,-1,-1,-1,-1,-1,9,-1],
				[3,8,-1,-1,-1,-1,-1,-1,-1],
				[-1,-1,-1,2,1,-1,-1,-1,6],
				[-1,-1,-1,-1,-1,-1,-1,-1,4],
				[-1,-1,4,5,-1,-1,7,-1,2],
				[-1,-1,7,-1,-1,9,-1,8,-1],
				[-1,-1,-1,-1,-1,7,-1,-1,-1]
		]

	prefilled = [ [ False for i in range(0, 9) ] for j in range(0, 9) ]

	for i in range(0,9):
		for j in range(0, 9):
			if start[i][j] != -1:
				prefilled[i][j] = True

	stk = []
	i, j = 0, 0
	s = sudokuState(start, i, j)
	while(prefilled[i][j]):
		i, j = s.next()
		s = sudokuState(start, i, j)
	s.m[i][j] = 1
	while not s.isValid():
		s.m[i][j] += 1

	stk.append(s)

	while not stk[-1].isWin():
		i, j = stk[-1].next()
		s = sudokuState(stk[-1].m, i, j)
		while(prefilled[i][j]):
			i, j = s.next()
			s = sudokuState(stk[-1].m, i, j)
		s.m[i][j] = 1
		flag = True
		while not s.isValid():
			s.m[i][j] += 1
			if s.m[i][j] == 10:
				flag = False
				while True:
					while stk[-1].m[stk[-1].r][stk[-1].c] == 9:
						stk.pop()
					stk[-1].m[stk[-1].r][stk[-1].c] += 1
					if stk[-1].isValid():
						break

		if flag:
			stk.append(s)

	f = open('sudoku.txt', 'w')
	s = sudokuState(start, 0, 0)
	print(s, file=f)
	print('\n-----------------------------------------------------------------\n', file=f)
	print(stk[-1], end='', file=f)
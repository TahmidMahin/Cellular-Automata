import pygame as pg

pg.init()
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
grey = (127, 127, 127)

height = 800
width = 1610

screen = pg.display.set_mode((width, height))
pg.display.set_caption("Cellular Automata")
font = pg.font.SysFont('Liberation Serif', 32, True, False)

grid = []
rules = []

class grid_cell:
	def __init__(self, x, y, cell_length):
		self.x = x
		self.y = y
		self.cell_length = cell_length
		self.cell_color = black

	def toggle_state(self):
		if self.cell_color == black:
			self.cell_color = yellow
		else:
			self.cell_color = black

	def show_cell(self):
		pg.draw.rect(screen, self.cell_color, (self.x,self.y,self.cell_length,self.cell_length))

def make_grid(length):
	for y in range(0, height, length):
		row = []
		for x in range(0, width, length):
			row.append(grid_cell(x+1, y+1, length-2))
		grid.append(row)

def show_grid():
	for row in grid:
		for cell in row:
			cell.show_cell()

def check(row, col):
	bin_string = ""
	for i in range(-1, 2):
		bin_string += "0" if grid[row-1][col+i].cell_color==black else "1"
	return int(bin_string, 2)

def simulate(ind):
	rule = rules[ind]
	grid[0][len(grid[0])//2-1].toggle_state()
	for i in range(1, len(grid)):
		for j in range(len(grid[0])//2-i-1, len(grid[0])//2+i):
			if rule[check(i, j)]:
				grid[i][j].toggle_state()

def make_rules():
	for num in range(255, -1, -1):
		bin_string = bin(num).replace("0b", "").rjust(8, "0")
		rule = []
		for letter in bin_string:
			rule.append(False if letter=="0" else True)
		rules.append(rule)

def initialize():
	running = True
	length = 10
	rule = 30
	make_grid(length)
	simulate(rule)
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP and length <= 20:
					length += 1
					grid.clear()
					make_grid(length)
					simulate(rule)
				if event.key == pg.K_DOWN and length >= 3:
					length -= 1
					grid.clear()
					make_grid(length)
					simulate(rule)
				if event.key == pg.K_RIGHT:
					rule += 1
					if rule == 256:
						rule = 0
					grid.clear()
					make_grid(length)
					simulate(rule)
				if event.key ==  pg.K_LEFT and rule >= 0:
					rule -= 1
					if rule == -1:
						rule = 255
					grid.clear()
					make_grid(length)
					simulate(rule)

		screen.fill(grey)
		show_grid()
		text = font.render("Rule : " + str(rule), False, white, black)
		screen.blit(text, (10, 10))
		pg.display.update()

make_rules()
initialize()
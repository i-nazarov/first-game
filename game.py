import pygame
import random
import sys

pygame.init()
Run = True
FPS = 60

SPC = 20
BLOCK_LEN = 20
W_WIDTH = 400
W_HEIGHT = 600
STEP = 20
SPEED = 1 / STEP
X_FIELD = [i for i in range(SPC, W_WIDTH, 20)]
COLORS = {'white': (255, 255, 255), 'black': (0, 0, 0)}
BORDERS_X = [SPC, W_WIDTH]

FRAME = pygame.display.set_mode((W_WIDTH+2*SPC, W_HEIGHT+2*SPC))
clock = pygame.time.Clock()
FRAME.fill(COLORS['black'])
pygame.display.update()
BG = pygame.Surface((W_WIDTH+SPC, W_HEIGHT+SPC))
BG.fill(COLORS['white'])
FRAME.blit(BG, (SPC/2, SPC/2))


class Event:
	def __init__(self):
		self.stop_event = False


class KeyPressure(Event):
	def __init__(self):
		self.pressed_keys = set()

	def record(self):
		while not self.stop_event:
			self.pressed_keys.add(pygame.key.get_pressed())


class Figure:
	def __init__(self):
		self.fig_cord = []

	def draw(self):
		for x, y in self.fig_cord:
			pygame.draw.rect(FRAME, COLORS['black'], (x, y, BLOCK_LEN, BLOCK_LEN))
			pygame.display.update()

	def move(self, side='down'):
		for block in self.fig_cord:
			x, y = block
			if side == 'down':
				block[1] += BLOCK_LEN / 20
			elif side == 'right':
				block[0] += BLOCK_LEN
			elif side == 'left':
				block[0] -= BLOCK_LEN
			pygame.draw.rect(FRAME, COLORS['black'], (x, y, BLOCK_LEN, BLOCK_LEN))
		pygame.display.update()
		FRAME.fill(COLORS['black'])
		FRAME.blit(BG, (SPC / 2, SPC / 2))

	def get_extr_coords(self):
		x_cords = [c[0] for c in self.fig_cord]
		min_x = min(x_cords)
		max_x = max(x_cords)
		return min_x, max_x


class Line(Figure):
	def __init__(self):
		self.flag = True
		first_x = random.choice(X_FIELD)
		self.xs = [first_x + i * BLOCK_LEN for i in range(4)]
		self.ys = [SPC for _ in range(4)]
		self.fig_cord = [[self.xs[i], self.ys[i]] for i in range(4)]

	def rotate(self):
		for block_num in range(len(self.fig_cord)):
			x, y = self.fig_cord[block_num]
			if self.flag:
				self.fig_cord[block_num] = [self.fig_cord[0][0], y + BLOCK_LEN*block_num]
			else:
				self.fig_cord[block_num] = [x + BLOCK_LEN*block_num, self.fig_cord[0][1]]

		self.flag = not self.flag


fig = None
while Run:
	for event in pygame.event.get():
		keys = pygame.key.get_pressed()
		if event.type == pygame.QUIT:
			Run = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				fig.rotate()
			elif event.key == pygame.K_RIGHT:
				rightmost = fig.get_extr_coords()[1]
				if rightmost not in BORDERS_X:
					fig.move('right')
			elif event.key == pygame.K_LEFT:
				leftmost = fig.get_extr_coords()[0]
				if leftmost not in BORDERS_X:
					fig.move('left')
	if not fig or fig.fig_cord[0][1] > W_HEIGHT:
		fig = Line()
		fig.draw()
	else:
		fig.move()
		clock.tick(FPS)



sys.exit()

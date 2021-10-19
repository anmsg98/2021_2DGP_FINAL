from pico2d import *
import GameFramework

class Mario:
	# State
	LEFT_IDLE, RIGHT_IDLE, LEFT_RUN, RIGHT_RUN,	LEFT_JUMP, RIGHT_JUMP, DIE = range(7)
	JUMP = 900
	GRAVITY = 3000

	KEY_MAP = {
		(SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
		(SDL_KEYDOWN, SDLK_RIGHT): (1,  0),
		(SDL_KEYUP, SDLK_LEFT):    (1,  0),
		(SDL_KEYUP, SDLK_RIGHT):   (-1,  0)
	}

	KEY_SPACE = (SDL_KEYDOWN, SDLK_SPACE)


	IMAGE_RECT = [
		# Left Idle
		[(360, 346, 30, 30)],
		# Right Idle
		[(420, 346, 30, 30)],
		# Left Run
		[(298, 346, 29, 30), (240, 346, 25, 30), (175, 346, 35, 30)],
		# Right Run
		[(480, 346, 29, 30), (542, 346, 25, 30), (598, 346, 33, 30)],
		# Left Jump
		[(57, 346, 34, 30)],
		# Right Jump
		[(717, 346, 34, 30)],
		# Die
		[(245, 4, 57, 78), (324, 6, 57, 80)]
	]

	def __init__(self):
		self.x, self.y = (100, 90)
		self.dx, self.dy = (0, 0)
		self.speed = 3
		self.fidx = 0
		self.time = 0
		self.jump_speed = 0
		self.state = Mario.RIGHT_IDLE
		self.image = load_image("resource/Mario.png")
		self.is_collide = False

	def draw(self):
		self.image.clip_draw(*Mario.IMAGE_RECT[self.state][self.fidx], self.x, self.y, 60, 60)

	def set_background(self, bg):
		self.set_background = bg

	def update(self):
		print(self.state)
		self.x += self.speed * self.dx
		self.fidx = int(self.time * 7) % len(Mario.IMAGE_RECT[self.state])
		self.time += GameFramework.delta_time
		if self.state in [Mario.RIGHT_JUMP, Mario.LEFT_JUMP]:
			self.y += self.falling_speed * GameFramework.delta_time
			self.falling_speed -= Mario.GRAVITY * GameFramework.delta_time
			if self.y < 90:
				self.y = 90
				self.falling_speed = 0
				if self.state == Mario.LEFT_JUMP:
					self.state = Mario.LEFT_RUN if self.dx < 0 else Mario.LEFT_IDLE
				elif self.state == Mario.RIGHT_JUMP:
					self.state = Mario.RIGHT_RUN if self.dx > 0 else Mario.RIGHT_IDLE

	def jump(self):
		if self.state in [Mario.LEFT_IDLE, Mario.LEFT_RUN]:
			self.state = Mario.LEFT_JUMP
			self.falling_speed = Mario.JUMP
			# print(get_time())
		elif self.state in [Mario.RIGHT_IDLE, Mario.RIGHT_RUN]:
			self.state = Mario.RIGHT_JUMP
			self.falling_speed = Mario.JUMP
			# print(get_time())

	def update_delta(self, ddx, ddy):
		dx, dy = self.dx, self.dy
		dx += ddx

		if ddx != 0:
			if self.state == Mario.LEFT_JUMP:
				if dx > 0: self.state = Mario.RIGHT_JUMP
			elif self.state == Mario.RIGHT_JUMP:
				if dx < 0: self.state = Mario.LEFT_JUMP
			else:
				self.state = \
					Mario.LEFT_RUN if dx < 0 else \
						Mario.RIGHT_RUN if dx > 0 else \
							Mario.LEFT_IDLE if ddx > 0 else Mario.RIGHT_IDLE

		dy += ddy
		self.dx, self.dy = dx, dy

	def handle_event(self, event):
		pair = (event.type, event.key)
		if pair in Mario.KEY_MAP:
			self.update_delta(*Mario.KEY_MAP[pair])
		elif pair == Mario.KEY_SPACE:
			self.jump()

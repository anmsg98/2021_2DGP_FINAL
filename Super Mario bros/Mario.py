from pico2d import *
import GameFramework

class Mario:
	# State
	LEFT_IDLE, RIGHT_IDLE, LEFT_RUN, RIGHT_RUN,	LEFT_JUMP, RIGHT_JUMP = range(6)
	JUMP = 900
	GRAVITY = 3000
	MAX_FIRE = 10
	KEY_MAP = {
		(SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
		(SDL_KEYDOWN, SDLK_RIGHT): (1,  0),
		(SDL_KEYUP, SDLK_LEFT):    (1,  0),
		(SDL_KEYUP, SDLK_RIGHT):   (-1,  0)
	}

	KEY_JUMP = (SDL_KEYDOWN, SDLK_SPACE)
	KEY_LIFE1 = (SDL_KEYDOWN, SDLK_1)
	KEY_LIFE2 = (SDL_KEYDOWN, SDLK_2)
	KEY_LIFE3 = (SDL_KEYDOWN, SDLK_3)
	KEY_FIRE = (SDL_KEYDOWN, SDLK_w)
	IMAGE_LIFE1 = [
		# Left Idle
		[[360, 346, 30, 30]],
		# Right Idle
		[[420, 346, 30, 30]],
		# Left Run
		[[298, 346, 29, 30], [240, 346, 25, 30], [175, 346, 35, 30]],
		# Right Run
		[[480, 346, 29, 30], [542, 346, 25, 30], [598, 346, 33, 30]],
		# Left Jump
		[[57, 346, 34, 30]],
		# Right Jump
		[[717, 346, 34, 30]]
	]
	IMAGE_LIFE2 = [
		# Left Idle
		[[359, 210, 33, 64]],
		# Right Idle
		[[417, 210, 33, 64]],
		# Left Run
		[[298, 210, 33, 64], [240, 210, 30, 64], [179, 210, 33, 64]],
		# Right Run
		[[476, 210, 33, 64], [538, 210, 30, 64], [597, 210, 33, 64]],
		# Left Jump
		[[59, 210, 32, 64]],
		# Right Jump]
		[[716, 210, 32, 64]]
	]
	IMAGE_FIREMAN = [
		# Left Idle
		[[359, 69, 33, 64]],
		# Right Idle
		[[417, 69, 33, 64]],
		# Left Run
		[[303, 69, 33, 64], [255, 69, 30, 64], [203, 69, 33, 64], [153, 69, 33, 64]],
		# Right Run
		[[472, 69, 33, 64], [524, 69, 30, 64], [573, 69, 33, 64], [622, 69, 33, 64]],
		# Left Jump
		[[52, 69, 32, 64]],
		# Right Jump]
		[[723, 69, 32, 64]]
	]
	IMAGE_FIRE = [[593, 307, 17, 17], [621, 307, 17, 17], [649, 307, 17, 17], [677, 309, 17, 17]]

	def __init__(self):
		self.x, self.y = (100, 80)
		self.dx, self.dy = 0, 0
		self.fidx = 0
		self.time = 0
		self.jump_speed = 0
		self.speed = 3
		self.state = Mario.RIGHT_IDLE
		self.life = 0
		self.image = load_image("resource/Mario.png")

		self.fx, self.fy = [0 for i in range(Mario.MAX_FIRE)], [0 for i in range(Mario.MAX_FIRE)]
		self.fdx = [0 for i in range(Mario.MAX_FIRE)]
		self.fidfx = [0 for i in range(Mario.MAX_FIRE)]
		self.fire_count = 0
		self.shoot_image = load_image("resource/background.png")
		self.is_fire = [False for i in range(Mario.MAX_FIRE)]

	def draw(self):
		for i in range(Mario.MAX_FIRE):
			if self.is_fire[i] == True:
				self.shoot_image.clip_draw(*Mario.IMAGE_FIRE[self.fidfx[i]], self.fx[i], self.fy[i])
				if self.fx[i] > 800:
					self.is_fire[i] = False
		if self.life == 0:
			self.image.clip_draw(*Mario.IMAGE_LIFE1[self.state][self.fidx], self.x, self.y, 40, 40)
		elif self.life == 1:
			self.image.clip_draw(*Mario.IMAGE_LIFE2[self.state][self.fidx], self.x, self.y, 40, 80)
		elif self.life == 2:
			self.image.clip_draw(*Mario.IMAGE_FIREMAN[self.state][self.fidx], self.x, self.y, 40, 80)

	def set_background(self, bg):
		self.set_background = bg

	def update(self):
		self.x += self.speed * self.dx
		for i in range(Mario.MAX_FIRE):
			if self.is_fire[i] == True:
				self.fidfx[i] = (self.fidfx[i] + 1) % 4
				self.fx[i] += self.speed * self.fdx[i] * 2
		if self.life == 0:
			self.fidx = int(self.time * 7) % len(Mario.IMAGE_LIFE1[self.state])
		elif self.life == 1:
			self.fidx = int(self.time * 7) % len(Mario.IMAGE_LIFE2[self.state])
		elif self.life == 2:
			self.fidx = int(self.time * 7) % len(Mario.IMAGE_FIREMAN[self.state])
		self.time += GameFramework.delta_time
		if self.state in [Mario.RIGHT_JUMP, Mario.LEFT_JUMP]:
			self.y += self.falling_speed * GameFramework.delta_time
			self.falling_speed -= Mario.GRAVITY * GameFramework.delta_time
			if self.life == 0:
				if self.y < 80:
					self.y = 80
					if self.state == Mario.LEFT_JUMP:
						self.state = Mario.LEFT_RUN if self.dx < 0 else Mario.LEFT_IDLE
					elif self.state == Mario.RIGHT_JUMP:
						self.state = Mario.RIGHT_RUN if self.dx > 0 else Mario.RIGHT_IDLE
			else:
				if self.y < 100:
					self.y = 100
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
		elif pair == Mario.KEY_JUMP:
			self.jump()
		elif pair == Mario.KEY_LIFE1:
			self.life = 0
			self.y = 80
		elif pair == Mario.KEY_LIFE2:
			self.life = 1
			self.y = 100
		elif pair == Mario.KEY_LIFE3:
			self.life = 2
			self.y = 100
		elif pair == Mario.KEY_FIRE and self.life == 2:
			self.is_fire[self.fire_count] = True
			self.fx[self.fire_count], self.fy[self.fire_count] = self.x, self.y
			if self.state in [Mario.RIGHT_IDLE, Mario.RIGHT_JUMP, Mario.RIGHT_RUN]:
				self.fdx[self.fire_count] = 1
			else:
				self.fdx[self.fire_count] = -1
			self.fire_count = (self.fire_count + 1) % Mario.MAX_FIRE

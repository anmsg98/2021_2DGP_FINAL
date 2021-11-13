from pico2d import *
import GameFramework
import GameWorld
import GameObject

class Mario:
	# State
	LEFT_IDLE, RIGHT_IDLE, LEFT_RUN, RIGHT_RUN,	LEFT_JUMP, RIGHT_JUMP, RIGHT_DRIFT, LEFT_DRIFT = range(8)
	JUMP = 1200
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
	KEY_FIRE = (SDL_KEYDOWN, SDLK_LCTRL)
	KEY_STAR = (SDL_KEYDOWN, SDLK_e)

	IMAGE_LIFE1 = [
		[[360, 870, 30, 30]],  # Left Idle
		[[420, 870, 30, 30]],  # Right Idle
		[[298, 870, 29, 30], [240, 870, 25, 30], [175, 870, 35, 30]],  # Left Run
		[[480, 870, 29, 30], [542, 870, 25, 30], [598, 870, 33, 30]],  # Right Run
		[[57, 870, 34, 30]],  # Left Jump
		[[717, 870, 34, 30]],  # Right Jump
		[[120, 870, 29, 30]],  # Left Drift
		[[661, 870, 29, 30]],  # Right Drift
		# STAR
		[[360, 547, 30, 30], [360, 502, 30, 30], [360, 457, 30, 30]],  # Left Idle
		[[420, 547, 30, 30], [420, 502, 30, 30], [420, 457, 30, 30]],  # Right Idle
		[[298, 547, 29, 30], [240, 547, 25, 30], [175, 547, 35, 30]],  # Left Run
		[[480, 547, 29, 30], [542, 547, 25, 30], [598, 547, 33, 30]],  # Right Run
		[[57, 547, 34, 30], [57, 502, 34, 30], [57, 457, 34, 30]],  # Left Jump
		[[717, 547, 34, 30], [717, 502, 34, 30], [717, 457, 34, 30]],  # Right Jump
		[[119, 547, 29, 30], [120, 502, 29, 30], [120, 457, 29, 30]],  # Left Drift
		[[661, 547, 29, 30], [661, 502, 29, 30], [661, 457, 29, 30]]  # Right Drift
	]
	IMAGE_LIFE2 = [
		[[359, 732, 33, 64]],  # Left Idle
		[[417, 732, 33, 64]],  # Right Idle
		[[298, 732, 33, 64], [240, 732, 30, 64], [179, 732, 33, 64]],  # Left Run
		[[476, 732, 33, 64], [538, 732, 30, 64], [597, 732, 33, 64]],  # Right Run
		[[59, 732, 32, 64]],  # Left Jump
		[[716, 732, 32, 64]],  # Right Jump
		[[658, 732, 33, 64]],  # Left Drift
		[[119, 732, 33, 64]],  # Right Drift
		# STAR
		[[359, 380, 33, 64], [359, 305, 33, 64], [359, 230, 33, 64]],  # Left Idle
		[[417, 380, 33, 64], [417, 305, 33, 64], [417, 230, 33, 64]],  # Right Idle
		[[298, 380, 33, 64], [240, 380, 30, 64], [179, 380, 33, 64]],  # Left Run
		[[476, 380, 33, 64], [538, 380, 30, 64], [597, 380, 33, 64]],  # Right Run
		[[59, 380, 32, 64], [59, 305, 32, 64], [59, 230, 32, 64]],  # Left Jump
		[[716, 380, 32, 64], [716, 305, 32, 64], [716, 230, 32, 64]],  # Right Jump
		[[658, 380, 33, 64], [658, 305, 33, 64], [658, 230, 33, 64]], # Left Drift
		[[119, 380, 33, 64], [119, 305, 33, 64], [119, 230, 33, 64]]  # Right Drift
	]
	IMAGE_FIREMAN = [
		[[359, 592, 33, 64]],  # Left Idle
		[[417, 592, 33, 64]],  # Right Idle
		[[303, 592, 33, 64], [255, 592, 30, 64], [203, 592, 33, 64], [153, 592, 33, 64]],  # Left Run
		[[472, 592, 33, 64], [524, 592, 30, 64], [573, 592, 33, 64], [622, 592, 33, 64]],  	# Right Run
		[[52, 592, 32, 64]],  # Left Jump
		[[723, 592, 32, 64]],  # Right Jump
		[[673, 592, 33, 64]],  # LEFT Drift
		[[103, 592, 33, 64]],  # Right Drift
		# STAR
		[[359, 160, 33, 64], [359, 85, 33, 64], [359, 10, 33, 64]],  # Left Idle
		[[417, 160, 33, 64], [417, 85, 33, 64], [417, 10, 33, 64]],  # Right Idle
		[[303, 160, 33, 64], [255, 160, 30, 64], [203, 160, 33, 64], [153, 160, 33, 64]],  # Left Run
		[[472, 160, 33, 64], [524, 160, 30, 64], [573, 160, 33, 64], [622, 160, 33, 64]],  	# Right Run
		[[52, 160, 32, 64], [52, 85, 32, 64], [52, 10, 32, 64]],  # Left Jump
		[[723, 160, 32, 64], [723, 85, 32, 64], [723, 10, 32, 64]],  # Right Jump
		[[673, 160, 33, 64], [673, 85, 33, 64], [673, 10, 33, 64]],  # Left Drift
		[[103, 160, 33, 64], [103, 85, 33, 64], [103, 10, 33, 64]]  # Right Drift
	]
	IMAGE_STAR = [

	]
	IMAGE_FIRE = [[593, 307, 17, 17], [621, 307, 17, 17], [649, 307, 17, 17], [677, 309, 17, 17]]

	def __init__(self):
		self.x, self.y = (100, 80)
		self.dx, self.dy = 0, 0
		self.fidx = 0
		self.time = 0
		self.driftr, self.driftl = True, True
		self.jumping = False
		self.jump_speed = 0
		self.accel = 0.0
		self.speed = 3
		self.falling_speed = 0
		self.state = Mario.RIGHT_IDLE
		self.life = 0
		self.star = False
		self.image = load_image("resource/Mario.png")

		self.fx, self.fy = [0 for i in range(Mario.MAX_FIRE)], [0 for i in range(Mario.MAX_FIRE)]
		self.fdx = [0 for i in range(Mario.MAX_FIRE)]
		self.fidfx = [0 for i in range(Mario.MAX_FIRE)]
		self.fire_count = 0
		self.shoot_image = load_image("resource/background.png")
		self.is_fire = [False for i in range(Mario.MAX_FIRE)]

	def draw(self):
		draw_rectangle(*self.get_bb())
		for i in range(Mario.MAX_FIRE):
			if self.is_fire[i] == True:
				self.shoot_image.clip_draw(*Mario.IMAGE_FIRE[self.fidfx[i]], self.fx[i], self.fy[i])
				if self.fx[i] > 800:
					self.is_fire[i] = False
		if self.life == 0:
			if self.star == True:
				self.image.clip_draw(*Mario.IMAGE_LIFE1[self.state+8][self.fidx], self.x, self.y, 40, 40)
			else:
				self.image.clip_draw(*Mario.IMAGE_LIFE1[self.state][self.fidx], self.x, self.y, 40, 40)
		elif self.life == 1:
			if self.star == True:
				self.image.clip_draw(*Mario.IMAGE_LIFE2[self.state+8][self.fidx], self.x, self.y, 40, 80)
			else:
				self.image.clip_draw(*Mario.IMAGE_LIFE2[self.state][self.fidx], self.x, self.y, 40, 80)
		elif self.life == 2:
			if self.star == True:
				self.image.clip_draw(*Mario.IMAGE_FIREMAN[self.state+8][self.fidx], self.x, self.y, 40, 80)
			else:
				self.image.clip_draw(*Mario.IMAGE_FIREMAN[self.state][self.fidx], self.x, self.y, 40, 80)

	def set_background(self, bg):
		self.set_background = bg

	def update(self):
		if self.dx > 0:
			self.accel += 0.02
			self.x += self.speed * self.dx * self.accel
			if self.accel > 1.0:
				self.accel = 1.0
			if self.accel < 0.0:
				if self.accel >= -0.2:
					self.accel += 0.01
					self.state = Mario.RIGHT_RUN
				if self.driftl == True:
					if self.state not in [Mario.LEFT_JUMP, Mario.RIGHT_JUMP]:
						self.state = Mario.LEFT_DRIFT
					self.driftl, self.driftr = False, True
		elif self.dx < 0:
			self.x -= self.speed * self.dx * self.accel
			self.accel -= 0.02
			if self.accel < -1.0:
				self.accel = -1.0
			if self.accel > 0.0:
				if self.accel <= 0.2:
					self.accel -= 0.01
					self.state = Mario.LEFT_RUN
				if self.driftr == True:
					if self.state not in [Mario.LEFT_JUMP, Mario.RIGHT_JUMP]:
						self.state = Mario.RIGHT_DRIFT
					self.driftl, self.driftr = True, False
		elif self.dx == 0 and self.accel != 0.0:
			if self.accel <= 0.0:
				self.accel += 0.01
				self.x += self.speed * self.accel
				if self.accel > 0.0:
					self.accel = 0.0
			else:
				self.accel -= 0.01
				self.x += self.speed * self.accel
				if self.accel < 0.0:
					self.accel = 0.0

		(lh, foot, rh, head) = self.get_bb()

		# for platform in GameWorld.objects_at(GameWorld.layer.platform):
		# 	(left, bottom, right, top) = platform.get_bb()
		# 	print(GameObject.collides_box(self, platform), self.state)
		# 	if (GameObject.collides_box(self, platform)):
		# 		if rh >= left and lh < left and head > bottom and foot < top:
		# 			self.x -= (rh - left)
		# 			self.accel = 0
		# 			if self.state in [Mario.RIGHT_RUN, Mario.RIGHT_IDLE]:
		# 				self.state = Mario.RIGHT_IDLE
		#
		# 		elif lh <= right and rh >= right and head > bottom and foot < top:
		# 			self.x -= (rh - left)
		# 			self.accel = 0
		# 			if self.state in [Mario.LEFT_RUN, Mario.LEFT_IDLE]:
		# 				self.state = Mario.LEFT_IDLE
		#
		# 		elif head > bottom and foot < bottom and (rh >= left or lh <= right):
		# 			self.y -= (head-bottom) + 1
		# 			self.falling_speed = 0
		#
		# 		elif foot < top and head > top and (rh >= left or lh <= right):
		# 			if self.state in [Mario.RIGHT_JUMP, Mario.RIGHT_RUN, Mario.LEFT_DRIFT]:
		# 				self.state = Mario.RIGHT_RUN if self.dx > 0 else Mario.RIGHT_IDLE
		# 			if self.state in [Mario.LEFT_JUMP, Mario.LEFT_RUN, Mario.RIGHT_DRIFT]:
		# 				self.state = Mario.LEFT_RUN if self.dx < 0 else Mario.LEFT_IDLE
		# 			self.y += (top - foot)
		# 			self.falling_speed = 0
		#




		for i in range(Mario.MAX_FIRE):
			if self.is_fire[i] == True:
				self.fidfx[i] = int(self.time * 14) % len(Mario.IMAGE_FIRE)
				self.fx[i] += self.speed * self.fdx[i] * 2
		if self.life == 0:
			if self.star == True:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_LIFE1[self.state+8])
			else:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_LIFE1[self.state])
		elif self.life == 1:
			if self.star == True:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_LIFE2[self.state+8])
			else:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_LIFE2[self.state])
		elif self.life == 2:
			if self.star == True:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_FIREMAN[self.state+8])
			else:
				self.fidx = int(self.time * 10) % len(Mario.IMAGE_LIFE2[self.state])
		self.time += GameFramework.delta_time
		if self.state in [Mario.LEFT_JUMP, Mario.RIGHT_JUMP]:
			self.y += self.falling_speed * GameFramework.delta_time
			self.falling_speed -= Mario.GRAVITY * GameFramework.delta_time
		if self.life == 0:
			if self.y < 80:
				self.jumping = False
				self.y = 80
				if self.state == Mario.LEFT_JUMP:
					self.state = Mario.LEFT_RUN if self.dx < 0 else Mario.LEFT_IDLE
				elif self.state == Mario.RIGHT_JUMP:
					self.state = Mario.RIGHT_RUN if self.dx > 0 else Mario.RIGHT_IDLE
		else:
			if self.y < 100:
				self.jumping = False
				self.y = 100
				if self.state == Mario.LEFT_JUMP:
					self.state = Mario.LEFT_RUN if self.dx < 0 else Mario.LEFT_IDLE
				elif self.state == Mario.RIGHT_JUMP:
					self.state = Mario.RIGHT_RUN if self.dx > 0 else Mario.RIGHT_IDLE

	def jump(self):
		if self.state in [Mario.LEFT_IDLE, Mario.LEFT_RUN, Mario.RIGHT_DRIFT]:
			self.state = Mario.LEFT_JUMP
			self.falling_speed = Mario.JUMP
			# print(get_time())
		elif self.state in [Mario.RIGHT_IDLE, Mario.RIGHT_RUN, Mario.LEFT_DRIFT]:
			self.state = Mario.RIGHT_JUMP
			self.falling_speed = Mario.JUMP
			# print(get_time())

	def get_bb(self):
		(x, y) = self.x, self.y
		if self.life == 0:
			(w, h) = (Mario.IMAGE_LIFE1[self.state][self.fidx % len(Mario.IMAGE_LIFE1[self.state])][2] // 2, Mario.IMAGE_LIFE1[self.state][self.fidx % len(Mario.IMAGE_LIFE1[self.state])][3] // 2)
		else:
			(w, h) = (Mario.IMAGE_LIFE2[self.state][self.fidx % len(Mario.IMAGE_LIFE1[self.state])][2] // 2, Mario.IMAGE_LIFE2[self.state][self.fidx % len(Mario.IMAGE_LIFE2[self.state])][3] // 2)
		left = x - w
		bottom = y - h
		right = x + w
		top = y + h

		return (left, bottom, right, top)


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
		elif pair == Mario.KEY_STAR:
			if self.star == False:
				self.star = True
			else:
				self.star = False
		elif pair == Mario.KEY_FIRE and self.life == 2:
			self.is_fire[self.fire_count] = True
			self.fx[self.fire_count], self.fy[self.fire_count] = self.x, self.y
			if self.state in [Mario.RIGHT_IDLE, Mario.RIGHT_JUMP, Mario.RIGHT_RUN]:
				self.fdx[self.fire_count] = 1
			else:
				self.fdx[self.fire_count] = -1
			self.fire_count = (self.fire_count + 1) % Mario.MAX_FIRE

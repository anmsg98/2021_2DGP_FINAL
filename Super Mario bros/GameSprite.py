import json
import GameFramework
import GameWorld
import GameObject
from pico2d import *

sprite_image = None
BG_image = None
sprite_rects = {}

def load():
	global sprite_image, BG_image

	if (sprite_image is None):
		sprite_image = load_image("resource/background.png")

	if (BG_image is None):
		BG_image = load_image("resource/BG1.png")

		with open("JSON/ObjectRect.json") as file:
			data = json.load(file)

			for name in data:
				sprite_rects[name] = tuple(data[name])


def createObject(info, mario):
	# obj = clazz(info["name"], info["x"], info["y"], info["w"], info["h"])
	obj = None
	if ("MysteryBox" in info["name"]):
		obj = MysteryBox(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("block" in info["name"]):
		obj = Box(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("Flag" in info["name"]):
		obj = Flag(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("Coin" == info["name"]):
		obj = Coin(info["name"], info["x"], info["y"])
	elif ("Coin2" == info["name"]):
		obj = Coin2(info["name"], info["x"], info["y"])
	elif ("Goomba" == info["name"]):
		obj = Goomba(info["name"], info["x"], info["y"], mario)
	elif ("ladder" in info["name"]):
		obj = Ladder(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("mushroom" in info["name"]):
		obj = Mushroom(info["name"], info["x"], info["y"])
	else:
		obj = Platform(info["name"], info["x"], info["y"], info["w"], info["h"])

	return obj


class Platform:
	def __init__(self, name, x, y, w, h):
		self.name = name
		self.rect = sprite_rects[name]
		self.pos = (x, y)
		self.bg = None
		self.size = (w, h)

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		sprite_image.clip_draw_to_origin(*self.rect, cx, cy, *self.size)
	def update(self):
		pass

	def set_background(self, bg):
		self.bg = bg

	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right = x + w
		top = y + h

		return (left, bottom, right, top)


class Box:
	IMAGE_RECT = [
		(113, 195, 16, 16)
	]
	def __init__(self, name, x, y, w, h):
		self.name = name
		self.pos = [x, y]
		self.pre_y = self.pos[1]
		self.bg = None
		self.size = (w, h)
		self.is_collide = False
		self.fidx = 0
		self.time = 0

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		sprite_image.clip_draw_to_origin(*Box.IMAGE_RECT[0], cx, cy, *self.size)

	def update(self):
		if self.is_collide:
			self.time += GameFramework.delta_time
			if self.time <= 0.1:
				self.pos[1] += 200 * GameFramework.delta_time
			elif self.time > 0.1 and self.time < 0.2 :
				self.pos[1] -= 200 * GameFramework.delta_time
			else:
				self.time = 0.0
				self.pos[1] = self.pre_y
				self.is_collide = False;

	def set_background(self, bg):
		self.bg = bg

	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right = x + w
		top = y + h

		return (left, bottom, right, top)


class MysteryBox:
	IMAGE_RECT = [
		(26, 195, 16, 16),
		(42, 195, 16, 16),
		(58, 195, 16, 16),
		(74, 195, 16, 16)
	]
	def __init__(self, name, x, y, w, h):
		self.name = name
		self.pos = [x, y]
		self.pre_y = self.pos[1]
		self.bg = None
		self.size = (w, h)
		self.fidx = 0
		self.time = 0
		self.fidtime = 0
		self.is_collide = False
		self.active = True

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		if self.active:
			self.fidtime += GameFramework.delta_time
			self.fidx = round(self.fidtime * 10) % 3
		else:
			self.fidx = 3
		sprite_image.clip_draw_to_origin(*MysteryBox.IMAGE_RECT[self.fidx], cx, cy, *self.size)


	def update(self):
		if self.active:
			if self.is_collide:
				self.time += GameFramework.delta_time
				if self.time <= 0.1:
					self.pos[1] += 200 * GameFramework.delta_time
				elif self.time > 0.1 and self.time < 0.2:
					self.pos[1] -= 200 * GameFramework.delta_time
				else:
					self.time = 0.0
					self.pos[1] = self.pre_y
					self.is_collide = False;
					self.active = False;

	def set_background(self, bg):
		self.bg = bg

	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right = x + w
		top = y + h

		return (left, bottom, right, top)


class Coin:
	IMAGE_RECT = [
		[377, 274, 8, 14],
		[409, 274, 4, 14],
		[438, 274, 3, 14],
		[468, 274, 5, 14]
	]
	def __init__(self, name, x, y):
		self.name = name
		self.pos = [x, y]
		self.bg = None
		self.fidx = 0
		self.collide = False
		self.animation = 0
		self.speed = 300
		self.time = 0
		self.coin_sound = load_wav("resource/coin.wav")
		self.coin_sound.set_volume(40)

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		self.fidx = round(self.time * 10) % 4
		if self.collide:
			sprite_image.clip_draw_to_origin(*Coin.IMAGE_RECT[self.fidx], cx, cy,
											 Coin.IMAGE_RECT[self.fidx][2] * 3,  Coin.IMAGE_RECT[self.fidx][3] * 3)
	def set_background(self, bg):
		self.bg = bg

	def update(self):
		if self.collide:
			self.animation += GameFramework.delta_time
			if self.animation < 0.3:
				self.pos[1] += self.speed * GameFramework.delta_time
			elif self.animation >= 0.3 and self.animation < 0.6:
				self.pos[1] -= self.speed * GameFramework.delta_time
			else:
				self.collide = False
				GameWorld.remove(self)


	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = (Coin.IMAGE_RECT[0][2]*3 // 2, Coin.IMAGE_RECT[0][3]*3 // 2)

		left = x-w
		bottom = y
		right = x + 2.5*w
		top = y + h

		return (left, bottom, right, top)


class Coin2:
	IMAGE_RECT = [
		[377, 274, 8, 14],
		[409, 274, 4, 14],
		[438, 274, 3, 14],
		[468, 274, 5, 14]
	]
	def __init__(self, name, x, y):
		self.name = name
		self.pos = [x, y]
		self.bg = None
		self.fidx = 0
		self.collide = False
		self.animation = 0
		self.time = 0
		self.coin_sound = load_wav("resource/coin.wav")
		self.coin_sound.set_volume(10)

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		self.fidx = round(self.time * 10) % 4
		sprite_image.clip_draw_to_origin(*Coin2.IMAGE_RECT[self.fidx], cx, cy,
										 Coin2.IMAGE_RECT[self.fidx][2] * 3,  Coin2.IMAGE_RECT[self.fidx][3] * 3)
	def set_background(self, bg):
		self.bg = bg

	def update(self):
		if self.collide:
			self.pos[1] = 1000
			self.animation += GameFramework.delta_time
			if self.animation > 0.5:
				GameWorld.remove(self)


	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = (Coin2.IMAGE_RECT[0][2]*3 // 2, Coin2.IMAGE_RECT[0][3]*3 // 2)

		left = x-w
		bottom = y
		right = x + 2.5*w
		top = y + h

		return (left, bottom, right, top)


class Mushroom:
	IMAGE_RECT = [
		[432, 332, 17, 17]
	]

	def __init__(self, name, x, y):
		self.name = name
		self.pos = [x, y]
		self.y = y
		self.bg = None
		self.fidx = 0
		self.collide = False
		self.animation = 0
		self.active = False
		self.speed = 100
		self.time = 0
		self.sound = load_wav("resource/item.wav")
		self.sound.set_volume(100)

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		if self.collide or self.active:
			sprite_image.clip_draw_to_origin(*Mushroom.IMAGE_RECT[self.fidx], cx, cy,
											 Mushroom.IMAGE_RECT[self.fidx][2] * 2, Mushroom.IMAGE_RECT[self.fidx][3] * 2)

	def set_background(self, bg):
		self.bg = bg

	def update(self):
		if self.collide:
			self.animation += GameFramework.delta_time
			if self.pos[1] < self.y + 40:
				self.pos[1] += self.speed * GameFramework.delta_time
			else:
				self.pos[1] = self.y + 40
				self.collide = False
				self.active = True




	def get_bb(self):
		(x, y) = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		(w, h) = (Mushroom.IMAGE_RECT[0][2] * 2 // 2, Mushroom.IMAGE_RECT[0][3] * 2 // 2)

		left = x
		bottom = y
		right = x + 2 * w
		top = y + 2 * h

		return (left, bottom, right, top)


class Flag:
	IMAGE_RECT = [
		(160, 224, 16, 168),
		(127, 224, 16, 168),
		(93, 224, 16, 168),
		(60, 224, 16, 168),
		(27, 224, 16, 168)
	]

	def __init__(self, name, x, y, w, h):
		self.name = name
		self.pos = (x, y)
		self.bg = None
		self.collide = True
		self.size = (w, h)
		self.fidx = 0
		self.time = 0

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		if self.collide:
			self.time += GameFramework.delta_time
			self.fidx = round(self.time * 2) % 5
		else:
			self.fidx = 0
		sprite_image.clip_draw_to_origin(*Flag.IMAGE_RECT[self.fidx], cx, cy, *self.size)

	def update(self):
		pass

	def set_background(self, bg):
		self.bg = bg

	def get_bb(self):
		(x, y) = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right = x + w
		top = y + h

		return (left, bottom, right, top)


class Goomba:
	IMAGE_RECT = [
		(211, 247, 17, 17),
		(241, 247, 17, 17),
		(270, 251, 17, 10)
	]

	def __init__(self, name, x, y, mario):
		self.name = name
		self.pos = [x, y]
		self.bg = None
		self.move = False
		self.fidx = 0
		self.dir = -1
		self.time = 0
		self.speed = 100
		self.mario = mario
		self.is_collide = False

	def set_background(self, bg):
		self.bg = bg

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		if self.is_collide == False:
			self.fidx = round(self.time * 10) % 2
		else:
			self.fidx = 2
		sprite_image.clip_draw_to_origin(*Goomba.IMAGE_RECT[self.fidx], cx, cy,
										 Goomba.IMAGE_RECT[self.fidx][2] * 2, Goomba.IMAGE_RECT[self.fidx][3] * 2)
	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = (Goomba.IMAGE_RECT[self.fidx][2]*2 // 2, Goomba.IMAGE_RECT[self.fidx][3]*2 // 2)

		left = x
		bottom = y
		right = x + 2*w
		top = y + 2*h

		return (left, bottom, right, top)

	def update(self):
		if self.pos[0] - self.mario.x < 800:
			self.move = True
		if self.move and self.is_collide == False:
			self.pos[0] += self.dir * self.speed * GameFramework.delta_time


class Ladder:
	IMAGE_RECT = [
		[311, 336, 49, 8]
	]

	def __init__(self, name, x, y, w, h):
		self.name = name
		self.pos = [x, y]
		self.size = (w, h)
		self.bg = None
		self.fidx = 0
		self.dir = -1
		self.time = 0
		self.speed = 100

	def set_background(self, bg):
		self.bg = bg

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		sprite_image.clip_draw_to_origin(*Ladder.IMAGE_RECT[self.fidx], cx, cy, *self.size)

	def get_bb(self):
		(x, y) = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right = x + w
		top = y + h

		return (left, bottom, right, top)

	def update(self):
		if self.pos[0] < 6000:
			self.pos[1] += self.dir * self.speed * GameFramework.delta_time
			if self.pos[1] < -20:
				self.pos[1] = 600
		else:
			self.pos[1] -= self.dir * self.speed * GameFramework.delta_time
			if self.pos[1] > 600:
				self.pos[1] = 0


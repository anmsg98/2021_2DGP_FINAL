
import json
import GameFramework
from pico2d import *

sprite_image = None
BG_image = None
sprite_rects = {}

def load():
	global sprite_image, BG_image

	if (sprite_image is None):
		sprite_image = load_image("resource/background.png")

	if (BG_image is None):
		BG_image = load_image("resource/BG.png")

		with open("JSON/ObjectRect.json") as file:
			data = json.load(file)

			for name in data:
				sprite_rects[name] = tuple(data[name])


def createObject(info):
	# obj = clazz(info["name"], info["x"], info["y"], info["w"], info["h"])
	obj = None
	if ("MysteryBox" in info["name"]):
		obj = MysteryBox(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("Flag" in info["name"]):
		obj = Flag(info["name"], info["x"], info["y"], info["w"], info["h"])
	elif ("Coin" in info["name"]):
		obj = Coin(info["name"], info["x"], info["y"])
	elif ("Goomba" in info["name"]):
		obj = Goomba(info["name"], info["x"], info["y"])
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
		draw_rectangle(*self.get_bb())
	def update(self):
		pass

	def set_background(self, bg):
		self.bg = bg

	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = self.size

		left = x
		bottom = y
		right =  x + w
		top =  y + h

		return (left, bottom, right, top)

class MysteryBox:
	IMAGE_RECT = [
		(26, 195, 16, 16),
		(42, 195, 16, 16),
		(58, 195, 16, 16)
	]
	def __init__(self, name, x, y, w, h):
		self.name = name
		self.pos = (x, y)
		self.bg = None
		self.size = (w, h)
		self.fidx = 0
		self.time = 0

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		self.fidx = round(self.time * 10) % 3
		sprite_image.clip_draw_to_origin(*MysteryBox.IMAGE_RECT[self.fidx], cx, cy, *self.size)
		draw_rectangle(*self.get_bb())
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

class Coin:
	IMAGE_RECT = [
		(377, 274, 8, 14),
		(409, 274, 4, 14),
		(438, 274, 3, 14),
		(468, 274, 5, 14)
	]
	def __init__(self, name, x, y):
		self.name = name
		self.pos = (x, y)
		self.bg = None
		self.fidx = 0
		self.time = 0

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		self.fidx = round(self.time * 10) % 4
		sprite_image.clip_draw_to_origin(*Coin.IMAGE_RECT[self.fidx], cx, cy,
										 Coin.IMAGE_RECT[self.fidx][2] * 3,  Coin.IMAGE_RECT[self.fidx][3] * 3)

	def set_background(self, bg):
		self.bg = bg

	def update(self):
		pass

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
		self.size = (w, h)
		self.fidx = 0
		self.time = 0

	def draw(self):
		cx, cy = self.pos[0] - self.bg.window_left, self.pos[1] - self.bg.window_bottom
		self.time += GameFramework.delta_time
		self.fidx = round(self.time * 2) % 5
		sprite_image.clip_draw_to_origin(*Flag.IMAGE_RECT[self.fidx], cx, cy, *self.size)
		draw_rectangle(*self.get_bb())

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

	def __init__(self, name, x, y):
		self.name = name
		self.pos = (x, y)
		self.bg = None
		self.fidx = 0
		self.time = 0
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
		draw_rectangle(*self.get_bb())
	def get_bb(self):
		(x, y) = self.pos[0]-self.bg.window_left, self.pos[1]-self.bg.window_bottom
		(w, h) = (Goomba.IMAGE_RECT[self.fidx][2]*2 // 2, Goomba.IMAGE_RECT[self.fidx][3]*2 // 2)

		left = x
		bottom = y
		right = x + 2*w
		top = y + 2*h

		return (left, bottom, right, top)

	def update(self):
		pass

import json
import GameFramework
from pico2d import *

structure_image = None
sprite_rects = {}

def load():
	global structure_image

	if (structure_image is None):
		structure_image = load_image("resource/background.png")

		with open("JSON/ObjectRect.json") as file:
			data = json.load(file)

			for name in data:
				print(name)
				sprite_rects[name] = tuple(data[name])

class Sprite:
	def __init__(self, name, x, y, w, h):
		load()
		self.name = name
		self.rect = sprite_rects[name]
		self.pos = (x, y)
		self.size = (w, h)

	def draw(self):
		structure_image.clip_draw_to_origin(*self.rect, *self.pos, *self.size)

	def update(self):
		pass
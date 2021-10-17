from pico2d import *
import GameFramework

objects = [[], [], [], []] # Tile, Coin, Ladder, Mario
trashcan = []

def add(layer_index, object):
	objects[layer_index].append(object)

def remove(object):
	trashcan.append(object)

def update():
	for layer_objects in objects:
		for object in layer_objects:
			object.update()

	counts = list(map(len, objects))

	if (len(trashcan) > 0):
		empty_trashcan()

def draw():
	for layer_objects in objects:
		for object in layer_objects:
			object.draw()

def empty_trashcan():
	global trashcan

	for object in trashcan:
		objects.remove(object)
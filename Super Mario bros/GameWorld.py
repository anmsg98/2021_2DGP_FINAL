from pico2d import *
import GameFramework

stage_obj = [[], [], [], []]
trashcan = []

def add(layer_index, object):
	stage_obj[layer_index].append(object)

def remove(object):
	trashcan.append(object)

def update():
	for layer_objects in stage_obj:
		for object in layer_objects:
			object.update()

	counts = list(map(len, stage_obj))

	if (len(trashcan) > 0):
		empty_trashcan()

def draw():
	for layer_objects in stage_obj:
		for object in layer_objects:
			object.draw()

def empty_trashcan():
	global trashcan

	for object in trashcan:
		stage_obj.remove(object)

	trashcan = []
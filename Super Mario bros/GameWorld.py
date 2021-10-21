from pico2d import *
import GameFramework

curr_obj = []
stage_obj = []
trashcan = []


def game_init(layer_names):
    global stage_obj
    global layer

    layer = lambda: None
    layerIndex = 0

    for name in layer_names:
        stage_obj.append([])
        layer.__dict__[name] = layerIndex
        layerIndex += 1


def all_objects():
    for layer_obj in curr_obj:
        for object in layer_obj:
            yield object


def objects_at(layer_index):
    for object in curr_obj[layer_index]:
        yield object


def add(layer_index, object):
	stage_obj[layer_index].append(object)

def remove(object):
	trashcan.append(object)

def update():
	for object in all_objects():
		object.update()

	if (len(trashcan) > 0):
		empty_trashcan()

def draw():
	for object in all_objects():
		object.draw()

def empty_trashcan():
	global trashcan

	for layer_objects in curr_obj:
		try:
			layer_objects.remove(object)
		except ValueError:
			pass

	trashcan = []
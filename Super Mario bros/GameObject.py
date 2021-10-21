from pico2d import *
import GameWorld

def collides_box(a, b):
	(la, ba, ra, ta) = a.get_bb()
	(lb, bb, rb, tb) = b.get_bb()

	if la > rb: return False
	if ra < lb: return False
	if ba > tb: return False
	if ta < bb: return False

	return True

def draw_collision_box():
	for object in GameWorld.all_objects():
			if hasattr(object, 'get_bb'):
				draw_rectangle(*object.get_bb())

def get_pico2d_pos(event):
    return (event.x, get_canvas_height() - event.y - 1)

def point_in_rect(point, rect):
    (x, y) = point
    (l, b, r, t) = rect

    if x < l: return False
    if x > r: return False
    if y < b: return False
    if y > t: return False

    return True
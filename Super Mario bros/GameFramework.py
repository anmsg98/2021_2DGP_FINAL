from pico2d import *
import time

running = True
stack = None
frame_interval = 0.01
delta_time = 0

def quit():
	global running

	running = False

def run(state):
	global running
	global stack
	global delta_time

	stack = [state]

	open_canvas()
	state.enter()

	last_time = time.time()

	while (running):
		# inter-frame (delta) time
		current_time = time.time()
		delta_time = current_time - last_time
		last_time = current_time

		# event handling
		events = get_events()

		for event in events:
			stack[-1].handle_event(event)

		# game logicasdas
		stack[-1].update()

		# game rendering
		clear_canvas()
		stack[-1].draw()
		update_canvas()

		delay(frame_interval)

	while (len(stack) > 0):
		stack[-1].exit()
		stack.pop()

	close_canvas()

def change(state):
	global stack

	if (len(stack) > 0):
		stack[-1].exit()
		stack.pop()

	stack.append(state)
	state.enter()

def push(state):
	global stack

	if(len(stack) > 0):
		stack[-1].pause()

	stack.append(state)
	state.enter()

def pop():
	global stack

	state_len = len(stack)

	if (state_len == 1):
		quit()
	elif (state_len > 1):
		stack[-1].exit()
		stack.pop()
		stack[-1].resume()

def run_main():
	import sys

	main_module = sys.modules["__main__"]
	run(main_module)
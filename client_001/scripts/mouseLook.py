#Blender Game Engine 2.55 Simple Camera Look
#Created by Mike Pan: mikepan.com

# Use mouse to look around
# W,A,S,D key to walk around
# E and C key to ascend and decend

from bge import logic as G
from bge import render as R
from bge import events

speed = 0.1				# walk speed
sensitivity = 1.0		# mouse sensitivity

owner = G.getCurrentController().owner

# center mouse on first frame, create temp variables
if "oldX" not in owner:
	G.mouse.position = (0.5,0.5)
	owner["oldX"] = 0.0
	owner["oldY"] = 0.0

else:
	x= 0.5 - G.mouse.position[0]
	y = 0.5 - G.mouse.position[1]
	
	x *= sensitivity
	y *= sensitivity
	
	# Smooth movement
	owner['oldX'] = (owner['oldX']*0.9 + x*0.1)
	owner['oldY'] = (owner['oldY']*0.9 + y*0.1)
	x = owner['oldX']
	y = owner['oldY']
	 
	# set the values
	owner.applyRotation([0, 0, x], False)
	owner.applyRotation([y, 0, 0], True)
	
	# Center mouse in game window
	G.mouse.position = (0.5,0.5)
	
	# keyboard control
	keyboard = G.keyboard.events
	if keyboard[events.WKEY]:
		owner.applyMovement([0,0,-speed], True)
	if keyboard[events.SKEY]:
		owner.applyMovement([0,0, speed], True)
	if keyboard[events.AKEY]:
		owner.applyMovement([-speed,0,0], True)
	if keyboard[events.DKEY]:
		owner.applyMovement([speed,0,0], True)
	if keyboard[events.EKEY]:
		owner.applyMovement([0,speed,0], True)
	if keyboard[events.CKEY]:
		owner.applyMovement([0,-speed,0], True)
###############################################
#
#  Customizable FPS Script (v2.3)
#   by Riyuzakisan (9/29/2011)
#   Made in Blender 2.59.0, r39307
#
#  Contact:
#   riyuzakisan@gmail.com
#  
#  Released under the Creative Commons
#  Attribution 3.0 Unported License.
#  
#  If you use this code, please include
#  this information header.
#
###############################################
'''
===============================================
||
||  This script includes:
||  -Mouselook
||  -Simple player movement (optional)
||	  -Location (static) movement
||	   OR
||	  -Dynamic movement
||  
===============================================
||  Instructions
===============================================
||
||  1. Add a Mouse: Movement sensor
||  (Doesn't need a specific name)
||
||  2. Add a Python controller and use this
||  script in the Script text line
||
||  3. Connect the Mouse sensor to the
||  python controller.
||
===============================================
||
||  To use as a Module:
||  1. Name the script: <script name>.py
||  2. Set the Python Controller to Module
||  3. Type your script name into the module
||	 like so:
||		  <script name>.main
||  
===============================================
||  Mouselook Configuration
===============================================
||
||  You can add the following properties to the
||  object using this mouselook script for additional
||  configuration options.
||  
||  "Property Name"   Type	  Value
||
||  "Adjust"	Integer 	#
||  -Sensitivity of the mouse
||  -Recommended: 2-3
||
||  "Invert"	Boolean 	True/False
||  -Invert the direction of the mouse movement
||
||  "Cap"	   Integer 		True/False
||  -Set the angle limit of looking up/down
||  -Use a value of 0-180
||
||  "Enable"	Boolean 	True/False
||  -Lets you Enable/Disable the mouselook script
||  -Useful for disabling mouselook on menu screens
||
||  "Cursor"	Boolean 	True/False
||  -Lets you Enable/Disable the mouse cursor
||
||  "UseParent" Boolean 	True/False
||  -Set if you want the parent of your script object
||   to inherit the Left/Right rotation from the script
||  Note:
||	  If you don't create this property, the parent
||	  object (by default) will receive the Left/Right
||	  rotation. This property is used to Disable that.
||
||	"Layout" 	Integer		1-2
||	-Use a value of 1 or 2 to set the keyboard layout
||		1: WASD, Space, Left Shift, E Q (Right handed)
||			-Suitable for Right Handed users
||		2: IJKL, Space, Right Shift, U O
||			-Suitable for Left Handed users
||	-If you put any other value, it will be set
||	 to 1 by default (WASD layout)
||  
===============================================
||  Location Movement Configuration
===============================================
||  
||  This simple movement system gives your
||  camera basic movement control without
||  having to set up a player object.
||  
||  This is designed for non-parented cameras.
||  IT WILL NOT WORK if the camera is parented
||  to another object!
||  
||  Requirements:
||  -Keyboard Sensor : True Pulse[```] : All Keys
||
||  Instructions:
||  1. Connect a Keyboard sensor to the script controller
||  Enable True Pulse [```], and Enable All Keys
||
||
||  Property Parameters:
||
||  "lMove" 	Boolean		True/False
||  -Set this to True to use Location Movement
||
||  "lSpeed"	Float		#.##
||  -Set the movement speed of the player
||  -Default: 0.05
||  -Controls: W S A D / I K J L
||
||  "lFly"		Float		#.##
||  -Set the fly speed of the player
||  -Default: 0.05
||  -Controls: Q E / O U
||			  
===============================================
||  Dynamic Movement Configuration
===============================================
||
||  This feature gives you the option to set up
||  dynamic movement for your player. The movement
||  uses Linear Velocity.
||  
||  Requirements:
||  -Keyboard Sensor : True Pulse [```] : All Keys
||  -Script object must have a Dynamic parent object
||  -If you want to jump, add these sensors to the
|| PARENT object and connect them to the script
|| controller:
||  -Collision sensor
||  -Ray sensor
||  Note: Sensors do not need to be named and will
||		auto-configure themselves
||
||  Instructions:
||  1. Connect a Keyboard sensor to the Script controller
||  Enable True Pulse [```], and Enable All Keys
||  
||  Property Parameters:
||  
||  "dMove" 	Boolean		True/False
||  -Set this to True to turn on Dynamic Movement
||
||  "dSpeed"	Integer 	#
||  -Set the movement speed of the player
||  -Default: 10
||  -Controls: W S A D / I K J L
||
||  "dJump" 	Integer		#
||  -Set the jump speed of the player
||  -Default: 10
||  -Controls: Space
||  -Requires: Collision and Ray sensors
||
||  "dRange"	Integer 	#
||  -Set the range for how close the player
||   must be to an object to jump (ray sensor)
||  -Default: 2
||
||	"dFly"		Boolean		True/False
||	-Set the option to jump and move without
||	 having to make contact with the ground
||
||	Crouching/Sneaking:
||		-Makes player move slower
||		-Controls: Left Shift / Right Shift
||
===============================================


===============================================
||  Thanks to
===============================================
||
||  -Blender Artist contributors for support
|| with the Game Engine
||
||  -Mouselook script from
|| tutorialsforblender3d.com
||
===============================================
'''

from bge import logic as l
from bge import render as r
from bge import events as e

def main():
	c = l.getCurrentController()
	o = c.owner
	
	#f = "Wetti"
	
	masterPiece = "Blender"
	
	# Default settings
	Sensitivity = 0.0005
	Invert = 1
	Capped = False
	Enable = True
	Cursor = False
	Useparent = False
	Parent = None
	
	# get game window size
	size = windowSize()
	
	# get the mouse movement sensor
	mouse = getMouse(c, o)
	
	# define mouse movement
	move = mouseMove(c, o, size, mouse)
	
	# get optional configuration from object properties
	sensitivity = mouseSen(o, Sensitivity)
	invert = mouseInv(o, Invert)
	capped = mouseCap(o, move, invert, Capped)
	enable = mouseEnable(o, Enable)
	parent = getParent(c, o, Parent)
	useparent = useParent(c, o, Useparent, parent)
	
	# take action
	showCursor(o, Cursor)
	mouseUse(c, o, move, sensitivity, invert, capped, enable, parent, useparent)
	mouseCenter(c, size, mouse, enable)
	
	# keyboard location movement
	useLoc(c, o)
	
	# keyboard movement
	dynamicMovement(o)
	
###############################################
	
def windowSize():
	width = r.getWindowWidth()
	height = r.getWindowHeight()
	
	return (width, height)

###############################################

def getMouse(c, o):
	mouse = None
	
	for i in c.sensors:
		if str(i.__class__) == "<class 'SCA_MouseSensor'>":
			if i.mode == 9:
				mouse = i
				
	return mouse

###############################################
	
def mouseMove(c, o, size, mouse):
	
	if mouse != None:
	
		width = size[0]
		height = size[1]
	
		x = width/2 - mouse.position[0]
		y = height/2 - mouse.position[1]
		
		if 'mousestart' not in o:
			o['mousestart'] = True
			x = 0
			y = 0
	
		if not mouse.positive:
			x = 0
			y = 0
			
		return (x, y)
	
###############################################
	
def mouseSen(o, sen):
	
	if 'Adjust' in o:
		if o['Adjust'] < 0.0:
			o['Adjust'] = 0.0
			
		sen = o['Adjust'] * sen
		
	return sen
			
############################################### 
			
def mouseInv(o, invert):
	
	if 'Invert' in o:
		if o['Invert'] == True:
			invert = -1
		else:
			invert = 1
			
	return invert 

###############################################
def mouseCap(o, move, invert, capped):
	
	if 'Cap' in o:
		import mathutils as m
		from math import pi
		
		if o['Cap'] > 180:
			o['Cap'] = 180
		if o['Cap'] < 0:
			o['Cap'] = 0
			
		camP = o.parent 
		camO = o.localOrientation
		
		camZ = [camO[0][2], camO[1][2], camO[2][2]]
		
		pZ = [0.0, 0.0, 1.0]
		
		v1 = m.Vector(camZ)
		v2 = m.Vector(pZ)
		
		rads = m.Vector.angle(v2, v1)
		angle = rads * (180.00 / pi)
		
		capAngle = o['Cap']
		
		moveY = move[1] * invert
		
		if (angle > (90 + capAngle/2) and moveY > 0) or (angle < (90 - capAngle/2) and moveY < 0) == True:
			
			capped = True
			
	return capped

###############################################

def mouseEnable(o, enable):
	
	if 'Enable' in o:
		if o['Enable'] == True:
			enable = True
		else:
			enable = False

	return enable

############################################### 
	
def showCursor(o, cursor):
	notset = False
	if 'Cursor' in o:
		if o['Cursor'] == True:
			cursor = True
		else:
			cursor = False
	else:
		# This is in case the player doesn't want the mouselook script
		# overriding their own cursor visibility settings
		notset = True
	
	if notset == False:
		if cursor == True:
			r.showMouse(1)
		else:
			r.showMouse(0)
	
###############################################

def getParent(c, o, parent):
	
	# if there is no parent, it returns None
	# which is the default anyway
	parent = o.parent
	return parent

###############################################

def useParent(c, o, useparent, parent):
	
	# useparent = False if o has no parent
	
	# if there is a parent
	if parent != None:
		
		# if there is no useparent property
		if 'UseParent' not in o:
			useparent = True
		else:
			if o['UseParent'] == True:
				useparent = True
			else:
				useparent = False
		
	# if there is no parent   
	if parent == None:
		useparent = False
					
	return useparent

# UseParent can only be set to True if there is a parent object
# if a parent is present, it will be used unless you create and set UseParent to False
	
###############################################
	
def mouseUse(c, o, move, sen, invert, capped, enabled, parent, useparent):
	
	if capped == True:
		vert = 0
	else:
		vert = move[1] * sen * invert
		
	horz = move[0] * sen * invert
	
	# Apply rotation values
	if enabled == True:
		ori = o.localOrientation.to_euler()
		ori.x += vert
		if useparent == False:
			ori.z += horz
		else:
			ori2 = parent.localOrientation.to_euler()
			ori2.z += horz
			parent.localOrientation = ori2
		o.localOrientation = ori
	
###############################################
	
def mouseCenter(c, size, mouse, enabled):
	
	if mouse != None:
		width = size[0]
		height = size[1]
		
		pos = mouse.position
		
		if pos != [int(width/2), int(height/2)]:
			if enabled != False:
				r.setMousePosition(int(width/2), int(height/2))   
			
###############################################

# meant for non-parented cameras
# lMove
def useLoc(c, o):
	if 'lMove' in o and o['lMove'] == True and o.parent == None:
		
		key = l.keyboard.events

		if 'lSpeed' in o:
			loc = o['lSpeed']
		else:
			loc = 0.05
		 
		if 'lFly' in o:
			fly = o['lFly']
		else:
			fly = 0.05
			
		layout = 1
		
		if 'Layout' in o:
			if o['Layout'] != 1 or o['Layout'] != 2:
				layout = 1
			if o['Layout'] == 1:
				layout = 1
			elif o['Layout'] == 2:
				layout = 2
		
		if layout == 1:
			up = key[e.WKEY] == 2
			down = key[e.SKEY] == 2
			left = key[e.AKEY] == 2
			right = key[e.DKEY] == 2
			
			flyUp = key[e.QKEY] == 2
			flyDown = key[e.EKEY] == 2
		elif layout == 2:
			up = key[e.IKEY] == 2
			down = key[e.KKEY] == 2
			left = key[e.JKEY] == 2
			right = key[e.LKEY] == 2
			
			flyUp = key[e.OKEY] == 2
			flyDown = key[e.UKEY] == 2
		 
		move = [0, 0, 0]
		fmove = [0, 0, 0]
		 
		# Up
		if up:
			move[2] = -loc

		# Down
		if down:
			move[2] = loc
		 
		# Left  
		if left:
			move[0] = -loc
		 
		# Right  
		if right:
			move[0] = loc
		 
		# Fly up
		if flyUp:
			fmove[2] = fly
		 
		# Fly down
		if flyDown:
			fmove[2] = -fly
		 
		o.applyMovement(move, True)
		o.applyMovement(fmove, False)
					
###############################################

# dMove
def dynamicMovement(own):
	if own.parent != None:
		if 'dMove' in own and own['dMove'] == True:
			o = own.parent
			k = l.keyboard.events
			
			layout = 1
			fly = False
			
			if 'Layout' in own:
				if own['Layout'] != 1 or own['Layout'] != 2:
					layout = 1
				if own['Layout'] == 1:
					layout = 1
				elif own['Layout'] == 2:
					layout = 2
			
			if 'dFly' in own:
				if own['dFly'] == True:
					fly = True
				else:
					fly = False
			
			if layout == 1:
				up = k[e.WKEY] == 2
				down = k[e.SKEY] == 2
				left = k[e.AKEY] == 2
				right = k[e.DKEY] == 2
				
				jump = k[e.SPACEKEY] == 2
				crouch = k[e.LEFTSHIFTKEY] == 2
			elif layout == 2:
				up = k[e.IKEY] == 2
				down = k[e.KKEY] == 2
				left = k[e.JKEY] == 2
				right = k[e.LKEY] == 2
				
				jump = k[e.SPACEKEY] == 2
				crouch = k[e.RIGHTSHIFTKEY] == 2
				
			col = None
			ray = None
			#"<class 'KX_TouchSensor'>"
			#"<class 'KX_RaySensor'>"
			for i in o.sensors:
				if str(i.__class__) == "<class 'KX_TouchSensor'>":
					col = i
				if str(i.__class__) == "<class 'KX_RaySensor'>":
					ray = i
			
			rray = False
			ccol = False
			
			if ray != None:
				ray.range = 2
				if 'dRange' in own:
					ray.range = own['dRange']
				ray.axis = 5
				# 5 = -Z axis
				
				if ray.positive:
					rray = True
			
			if col != None:
				if col.positive:
					ccol = True
			
			speed = 10
			jspeed = 0
			jumpspeed = 10
			limit = .75
			
			if 'dSpeed' in own:
				speed = own['dSpeed']
			if 'dJump' in own:
				jumpspeed = own['dJump']
			
			if crouch and o['air'] == False:
				speed = speed/3
				limit = .95
				
			fspeed = speed * (up - down)
			sspeed = speed * (right - left)
			
			if fspeed and sspeed:
				fspeed *= 0.70710678
				sspeed *= 0.70710678
			
			if 'air' not in o:
				o['air'] = False
				
			if (o['air'] == True or not ccol) and fly == False:
				fspeed *= .005
				sspeed *= .005
			
			if jump and o['air'] == False and rray and not crouch:
				jspeed = jumpspeed
				o['air'] = True
			
			if jump and fly == True:
				jspeed = 1
				
			elif ccol and not jump:
				o['air'] = False
			
			o.localLinearVelocity[0] += sspeed
			o.localLinearVelocity[1] += fspeed
			o.localLinearVelocity[2] += jspeed
			
			for i in o.localLinearVelocity:
				ind = list(o.localLinearVelocity).index(i)
				if ind != 2:
					if i > speed:
						i = speed
					if i < -speed:
						i = -speed
				o.localLinearVelocity[ind] = i
			
			if o['air'] == False:
				if not up and not down:
					o.localLinearVelocity[1] -= o.localLinearVelocity[1]*limit
				if not left and not right:
					o.localLinearVelocity[0] -= o.localLinearVelocity[0]*limit
			elif o['air'] == True and fly == False:
				for i in o.localLinearVelocity:
					ii = i*0.02
					ind = list(o.localLinearVelocity).index(i)
					if ind != 2:
						o.localLinearVelocity[ind] += ii
			if fly == True and crouch == True:
				o.localLinearVelocity[2] = 0
				
###############################################
					
# If script is not set as a module, it will run this way
main()
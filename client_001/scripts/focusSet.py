
from bge import logic as G
from bge import render as R
from bge import events

own = G.getCurrentController().owner

# init
if "focaltarget" not in own:
	own["focaltarget"] = 0.98

if G.mouse.events[events.WHEELUPMOUSE]:
	own["focaltarget"] +=0.02
if G.mouse.events[events.WHEELDOWNMOUSE]:
	own["focaltarget"] -=0.02


if own["focaltarget"] < 0.1: own["focaltarget"] = 0.1
if own["focaltarget"] > 1.0: own["focaltarget"] = 1.0

#then always blend, for smooth transition
own["focus"] = own["focaltarget"] * 0.1 + own["focus"]*0.9
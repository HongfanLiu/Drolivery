import runWorld as rw
import drawWorld as dw
import pygame as pg
from random import randint

################################################################

# This program is an interactive simulation/game. A cat starts
# to move across the screen. The direction of movement is reversed
# on each "mouse down" event.
#
# The state of the cat is represented by a tuple (pos, delta-pos).
# The first element, pos, represents the x-coordinate of the cat.
# The second element, delta-pos, represents the amount that the
# position changes on each iteration of the simulation loop.
#
# For example, the tuple (7,1) would represent the cat at x-coord,
# 7, and moving to the right by 1 pixel per "clock tick."
#
# The initial state of the cat in this program is (0,1), meaning that the cat
# starts at the left of the screen and moves right one pixel per tick.
#
# Pressing a mouse button down while this simulation run updates the cat state
# by leaving pos unchanged but reversing delta-pos (changing 1 to -1 and vice
# versa). That is, pressing a mouse key reverses the direction of the
# cat.
#
# The simulation ends when the cat is allowed to reach either the left
# or the right edge of the screen.

################################################################

# Global variables
touchRange = ([], [])
score = 0

# Static variables
droneSize = 48
deliverySize = 16

# Initialize world
name = "Drolivery - Fast & Accurate Drone Delivery"
width = 1024
height = 700
rw.newDisplay(width, height, name)

################################################################

# Display the state by drawing a cat at that x coordinate
droneImage = dw.loadImage("drone.png")
deliveryImage = dw.loadImage("delivery.png")

# state -> image (IO)
# draw the cat halfway up the screen (height/2) and at the x
# coordinate given by the first component of the state tuple
#
def updateDisplay(state):
    dw.fill(dw.white)
    dw.draw(droneImage, (state[0], state[2]))
    dw.draw(deliveryImage, (deliveryInitState[0], deliveryInitState[1]))

################################################################

# Change pos by delta-pos, leaving delta-pos unchanged
# Note that pos is accessed as state[0], and delta-pos
# as state[1]. Later on we'll see how to access state
# components by name (as we saw with records in Idris).
#
# state -> state
def updateState(state):
    global score
    score += 1
    return((state[0] + state[1], state[1], state[2] + state[3], state[3]))

################################################################

# Terminate the simulation when the x coord reaches the screen edge,
# that is, when pos is less then zero or greater than the screen width
# state -> bool
def endState(state):
    return (end(state))


def end(state):
    return touching(state) or state[0] > (width - droneSize) or state[2] > (height - droneSize) or state[0] < 0 or state[2] < 0


def touching(state):
    for i in droneBoundaries(state[0]):
        if (i in touchRange[0]):
            for j in droneBoundaries(state[2]):
                if (j in touchRange[1]):
                    return True

    return False

def droneBoundaries(axis):
    b = []
    for i in range(axis, axis + droneSize):
        b.append(i)

    return b

################################################################

# We handle each event by printing (a serialized version of) it on the console
# and by then responding to the event. If the event is not a "mouse button down
# event" we ignore it by just returning the current state unchanged. Otherwise
# we return a new state, with pos the same as in the original state, but
# delta-pos reversed: if the cat was moving right, we update delta-pos so that
# it moves left, and vice versa. Each mouse down event changes the cat
# direction. The game is to keep the cat alive by not letting it run off the
# edge of the screen.
#
# state -> event -> state
#
def handleEvent(state, event):
    if (event.type == pg.MOUSEBUTTONDOWN):
        newState = [randomSpeed(), randomSpeed()]
        return((state[0], newState[0], state[2], newState[1]))
    else:
        return(state)

def randomSpeed():
    r = randint(-7,7)
    if (r == 0):
        r = randomSpeed()

    return r

def randomAxys(min, max):
    return randint(min, max)
################################################################

# The cat starts at the left, moving right
#initState = (80, 1, 80, 1)
initState = (0, 3, randomAxys(0, (height-1)), 2)
deliveryInitState = (100, 100)
#deliveryInitState = (randomAxys(984, 1010), randomAxys(17, 682))

for i in range(deliveryInitState[0], deliveryInitState[0] + deliverySize):
    touchRange[0].append(i)

for i in range(deliveryInitState[1], deliveryInitState[1] + deliverySize):
    touchRange[1].append(i)

print(touchRange)
# Run the simulation no faster than 60 frames per second
frameRate = 60

# Run the simulation!
rw.runWorld(initState, updateDisplay, updateState, handleEvent, endState, frameRate)

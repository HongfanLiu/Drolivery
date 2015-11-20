import runWorld as rw
import drawWorld as dw
import pygame as pg
from random import randint

################################################################

# DESCRIPTION
# OF
# THE
# GAME

################################################################

# Global variables
touchRange = ([], [])
score = 0
scoreText = ""
scoreScreen = 0

# Static variables
DRONE_SIZE = 48
DELIVERY_SIZE = 16
WIDTH = 1024
HEIGHT = 700

# Initialize world
# TODO - instead of creating a new window for the scores, maybe just erase everything and change the title
name = "Drolivery - Fast & Accurate Drone Delivery"

rw.newDisplay(WIDTH, HEIGHT, name)

# Initialize font -> must be called after pygame.init() to avoid 'Font not Initialized' error
font = pg.font.Font(None, 35)

################################################################

# Loads the images
droneImage = dw.loadImage("drone.png")
deliveryImage = dw.loadImage("delivery.png")

"""
DOCUMENT
"""
def updateDisplay(state):
    dw.fill(dw.white)
    global scoreText

    if (scoreScreen == 0):
        dw.draw(droneImage, (state[0], state[2]))
        dw.draw(deliveryImage, (deliveryInitState[0], deliveryInitState[1]))
        scoreText = font.render("Score: " + str(score), 1, (0, 0, 0))
        dw.draw(scoreText, (WIDTH / 2, 5))
    else:
        name = "Score Window"
        if (scoreScreen == 1):
            scorePrint = font.render("Your score was: " + str(score),1,(0,0,0))
        else:
            scorePrint = font.render("Your score was: " + str(10000-score),1,(0,0,0))  
        dw.draw(scorePrint, ((WIDTH / 2)-100,HEIGHT/2))


################################################################

"""
DOCUMENT
"""
def updateState(state):
    if (scoreScreen == 0):
        global score
        score += 1
        return ((state[0] + state[1], state[1], state[2] + state[3], state[3]))
    return (0,0,0,0)

################################################################

"""
DOCUMENT
"""
def endState(state):
    global scoreScreen
    if (end(state) and scoreScreen == 0):
        scoreScreen = 1
    elif (touching(state)):
        scoreScreen = 2
        return False

    # Ends the game
    if (scoreScreen == 2):
        return True

    return False

def end(state):
    return state[0] > (WIDTH - DRONE_SIZE) or state[2] > (HEIGHT - DRONE_SIZE) or state[0] < 0 or state[2] < 0


"""
Checks whether or not any part of the drone touched any part of the delivery box
"""
def touching(state):
    for i in droneBoundaries(state[0]):
        if (i in touchRange[0]):
            for j in droneBoundaries(state[2]):
                if (j in touchRange[1]):
                    return True

    return False

"""
Retrieves all the pixels relative to the area that the drone covers
"""
def droneBoundaries(axis):
    b = []
    for i in range(axis, axis + DRONE_SIZE):
        b.append(i)

    return b

################################################################

"""
DOCUMENT
"""
def handleEvent(state, event):
    # TODO - catch the event handler to get the spacebar or some other key and set the state of the game var to true, the user can only change it when the previous game is ended
    if (event.type == pg.MOUSEBUTTONDOWN):
        newState = [randomSpeed(), randomSpeed()]
        return((state[0], newState[0], state[2], newState[1]))
    if (event.type == pg.K_SPACE and scoreScreen == 0):
        global scoreScreen
        scoreScreen = 2

    return(state)


"""
Generates a random speed value different from 0
"""
def randomSpeed():
    r = randint(-4,4)
    if (r == 0):
        r = randomSpeed()

    return r

"""
Generates a random number between the given boundaries
"""
def randomAxys(min, max):
    return randint(min, max)
################################################################

# The drone starts in a random position between the top and halfway of the screen
#initState = (80, 1, 80, 1)
initState = (0, 3, randomAxys(0, (HEIGHT - 350)), 2)
# The delivery box starts in a random position near the end of the screen to the right side
#deliveryInitState = (100, 100)
deliveryInitState = (randomAxys(984, 1010), randomAxys(17, 682))

"""
Fills the touchRange list with the delivery box boundaries
"""
def getDeliveryBoundaries():
    for i in range(deliveryInitState[0], deliveryInitState[0] + DELIVERY_SIZE):
        touchRange[0].append(i)
    for i in range(deliveryInitState[1], deliveryInitState[1] + DELIVERY_SIZE):
        touchRange[1].append(i)

# Filling the touchRange list
getDeliveryBoundaries()

# Run the simulation no faster than 60 frames per second
frameRate = 60

# Run the simulation!
rw.runWorld(initState, updateDisplay, updateState, handleEvent, endState, frameRate)

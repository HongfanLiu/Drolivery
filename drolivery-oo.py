import runWorld as rw
import drawWorld as dw
import pygame as pg
from random import randint

################################################################
'''
Don't you hate when you have to go all the way to the mail to get your package?
Or even when you have to wait for it to come by mail, and keep getting those annoying texts from the ups guy
saying that is close, but isn`t really...
The game objective is to get the drone to get the package, but is not that easy. The drone starts with an
random speed and each click you make causes the drone to radomly change the speed and the drone's trajectory.


HOW TO PLAY:
1 - CLICK ON THE SCEEN TO RAMDOMLY CHANGE THE DRONE'S SPEED AND TRAJECTORY
2 - IF YOU TOUCH THE BORDERS OF THE WINDOW, YOU LOSE
3 - WHEN THE DRONE TOUCHES THE PACKAGE YOU WIN!!
4 - HAVE FUN !!
'''
################################################################

# Global variables
touchRange = ([], [])
score = 0
scoreText = ""
# 0 - The game is being played, 1 = The player lost, 2 = The player won
gameState = 0

# Static variables
DRONE_SIZE = 48
DELIVERY_SIZE = 16
WIDTH = 1024
HEIGHT = 700

# Initialize world
name = "Drolivery - Fast & Accurate Drone Delivery"
rw.newDisplay(WIDTH, HEIGHT, name)

# Initialize font -> must be called after pygame.init() to avoid 'Font not Initialized' error
font = pg.font.Font(None, 35)

################################################################

# Loads the images
droneImage = dw.loadImage("drone.png")
deliveryImage = dw.loadImage("delivery.png")

"""
Update the display accordingly with the game state
"""
def updateDisplay(state):
    dw.fill(dw.white)
    global scoreText
    global name

    if (gameState == 0):
        dw.draw(droneImage, (state[0], state[2]))
        dw.draw(deliveryImage, (deliveryInitState[0], deliveryInitState[1]))
        scoreText = font.render("Score: " + str(score), 1, (0, 0, 0))
        dw.draw(scoreText, (WIDTH / 2, 5))
    else:
        name = "Score"
        if (gameState == 1):
            winLose = font.render("You LOST!",1,(0,0,0))
            scorePrint = font.render("Your score was: " + str(score),1,(0,0,0))
        else:
            winLose = font.render("You WON!",1,(0,0,0))
            scorePrint = font.render("Your score was: " + str(10000 - score),1,(0,0,0))

        restart = font.render("Press [Space Bar] to restart...",1,(0,0,0))

        dw.draw(scorePrint, ((WIDTH / 2) - 100, HEIGHT/2))
        dw.draw(winLose, ((WIDTH / 2) - 50, (HEIGHT / 2) - 80))
        dw.draw(restart, ((WIDTH / 2) - 150, (HEIGHT / 2) + 80))


################################################################

"""
Update the state of the game
"""
def updateState(state):
    if (gameState == 0):
        global score
        score += 1
        return [state[0] + state[1], state[1], state[2] + state[3], state[3]]
    return [0,0,0,0]

################################################################

"""
Checks wether or not the game ended, and updates the game state
"""
def endState(state):
    global gameState
    if (end(state) and gameState == 0):
        gameState = 1
    elif (touching(state)):
        gameState = 2
        return False

    return False
"""
Checks if the drone touched the window borders.
"""
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

"""
Handles the events and restart the game when needed
"""
def handleEvent(state, event):
    global gameState
    if (event.type == pg.MOUSEBUTTONDOWN):
        newState = [randomSpeed(), randomSpeed()]
        return((state[0], newState[0], state[2], newState[1]))
    if (event.type == pg.KEYDOWN and gameState != 0):
        if (event.key == pg.K_SPACE):
            restart(state)

    return state
"""
Restarts the game and his variables
"""
def restart(state):
    global deliveryInitState
    global gameState
    global score
    global touchRange

    state[0] = 0
    state[1] = 3
    state[2] = randomAxys(0, (HEIGHT - 350))
    state[3] = 2

    score = 0
    deliveryInitState = (randomAxys(984, 1010), randomAxys(17, 682))
    gameState = 0

    touchRange = ([], [])
    getDeliveryBoundaries()

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


class State:
    x_axis = 0
    x_speed = 3
    y_speed = 2

    def setYAxis(self, val):
        self.y_axis = val

    def __init__(self, val):
        self.setYAxis(val)


initState = State(randomAxys(0, (HEIGHT - 350)))

# The drone starts in a random position between the top and halfway of the screen
#initState = (x-axis: 0, x-speed: 3, y-axis: randomAxys(0, (HEIGHT - 350)), y-speed: 2)

# The delivery box starts in a random position near the end of the screen to the right side
#deliveryInitState = (x-axis: randomAxys(984, 1010), y-axis: randomAxys(17, 682))

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

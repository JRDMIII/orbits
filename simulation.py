import pygame
from body import Body
from universe import Universe
import random

from pygame.locals import *

# Initialising PyGame
pygame.init()

# Creating the universe
universe = Universe(
    g_const=(6.67430 * 10**(-11)),
    g_multiplier=10**10,
    colour=(0, 0, 0),
    size=(1000, 1000),
    damping_factor=0.9
)

# Defining dimension of the screen using the universe
SCREEN = pygame.display.set_mode(universe.size)

def random_body_generator(index):
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = random.randint(0, universe.size[0])
    y = random.randint(0, universe.size[1])
    name = f"Body {index}"
    mass = random.randint(10, 200)
    initial_velocity = ((random.random()-0.5)*2, (random.random()-0.5)*2)

    return Body(x, y, name, colour, mass, initial_velocity)

num_planets = 3

# Generating random planets and adding them to the universe
universe.add_bodies([random_body_generator(i) for i in range(num_planets)])

# universe.add_bodies([Planet(200, 200, "Black Hole", (10, 10, 10), 10000, (0.2, 0.01)), Planet(1000, 200, "Black Hole", (10, 10, 10), 10000, (-0.2, -0.01))])

clock = pygame.time.Clock()

# Flag to ensure the game continues to run
run = True

while run:
    # for loop through the event queue
    for event in pygame.event.get():
         
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
             
            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE:
                gameOn = False
                 
        # Check for QUIT event
        elif event.type == QUIT:
            gameOn = False

    # Remove all bodies from the screen
    SCREEN.fill(universe.UNVIERSE_COLOUR)

    # Update the velocity of each body
    for body in universe.bodies:
        body.update_velocity(universe)
    
    # Update the position of each body and draw it on the screen
    for body in universe.bodies:
        body.update_position(universe)
        body.draw(SCREEN)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(165)
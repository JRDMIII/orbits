import numpy as np
import pygame
from typing import Self
import math
from universe import Universe

class Body:
    def __init__(self, x: float, y: float, name: str, colour: tuple, mass: float, initial_velocity: tuple):
        # Current position of the body in the universe
        self.position = np.array([float(x), float(y)])

        # Name of the planet
        self.name = name

        # Mass of the body
        self.mass = mass

        # Calculating radius as a function of mass
        self.radius = min(100, max(mass, 10) / 2)

        # Colour of the body
        self.colour = colour

        # Current velocity of the body (x, y)
        self.current_velocity = np.array(initial_velocity)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.colour, (int(self.position[0]), int(self.position[1])), self.radius)
    
    def calculateDistance(self, body: Self):
        # Calculating square distance between two bodies as a vector
        square_dist = sum(pow(elem, 2) for elem in (body.position - self.position))

        return square_dist

    def calculateForce(self, body: Self, universe: Universe):
        # Calculating the force of gravity between two bodies
        force_dir = (body.position - self.position) / math.sqrt(self.calculateDistance(body))
    
        return (universe.GRAVITY_MULTIPLIER * force_dir * universe.GRAVITATIONAL_CONSTANT * self.mass * body.mass) / self.calculateDistance(body)

    def update_velocity(self, universe: Universe):
        # Looping through all bodies in the universe
        for body in universe.bodies:
            if body != self:
                # If the body is not this planet then calculate force
                force = self.calculateForce(body, universe)

                # Getting acceleration due to force
                acc = force / self.mass

                # Calculating new speed
                self.current_velocity += acc

        # Checking if speed has surpased the speed threshold of the universe
        if self.current_velocity[0] > universe.SPEED_THRESHHOLD:
            # We apply the damping factor in the case it is larger
            self.current_velocity[0] *= universe.DAMPING_FACTOR
        
        if self.current_velocity[1] > universe.SPEED_THRESHHOLD:
            self.current_velocity[1] *= universe.DAMPING_FACTOR
        
    def update_position(self, universe: Universe):
        # Updating the position of the body based on its current speed
        self.position += self.current_velocity

        # Checking if the body has gone out of bounds
        if self.position[0] < 0 or self.position[0] > universe.size[0]:
            self.position[0] = 0 if self.position[0] < 0 else universe.size[0] - 10
            self.current_velocity[0] *= -1

        if self.position[1] < 0 or self.position[1] > universe.size[1]:
            self.position[1] = 0 if self.position[1] < 0 else universe.size[1] - 10
            self.current_velocity[1] *= -1
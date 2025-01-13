# Orbits: A Physics Project
Recently I have been interested in creating simulations and doing them without the help of AI so I decided to create a rather simple simulation of planetary bodies and how their forces act on eachother. Even though the project is quite basic, the results should be rather fun to observe.

## The Theory
Between two planetary bodies, A and B, there is an attractive force that acts between them which is directly proportional to the mass of both bodies and inversely proportional to the square of the distance between the two planets. To calculate this force, we use the equation:

$$
F = \frac{Gm_Am_B}{r^2} \\
$$

Where: \
$F$ is the force applied to both planets \
$G$ is the gravitational constant \
$m_A$ is the mass of planet A \
$m_B$ is the mass of planet B \
$r$ is the distance between the centres of both planets

This is then applied to both planets in the direction of the other planet (along the vector which moves from the centre of that planet to the other). All objects with a mass apply this force to all other objects within the universe that have mass.

## The Design
In order to implement this in a simulation the main functionality that needs to be included is calculating the force applied to the bodies and applying those forced appropriately.

### Bodies
For each body, they should have these parameters:
1. Mass - The mass of the planet
2. Current Velocity - The current speed - split into x and y velocities - of the planet
3. Radius - Defines the size the planet will take when it is drawn

Other attributes can be added to it for extras however for now these should be sufficient to draw out the planets and apply forces to them.

### Universe
The universe will be what defines the constants and the dimensions of the simulation. It will also have an array of all the bodies which will allow for the calculations to be done on all the bodies at once.

### Forces and Angles
The first way I thought this could be implemented was calculating the force, then using the angle between the two planets to get the horizontal and vertical forces that should be applied. Those can then be applied to the horizontal and vertical speeds of the planets.

The issue with this is it requires a lot more computation as the force needs to be split into vectors using trigonometry as well as dot product to calculate the angles between planets. Another issue with this is calculating the relative angles as dot product flips to negative at 180 degrees.

With all this in mind, I decided to instead calculate the forces as a vector throughout the process so that the acceleration can simply be added to the velocity vector and the new velocities can be found. This should hopefully reduce the number of calculations that need to occur.

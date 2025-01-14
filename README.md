# Orbits: A Physics Project

![image](https://github.com/user-attachments/assets/220ceead-6070-493b-bac5-bd375b0b5029)

Recently I have been interested in creating simulations and doing them without the help of AI so I decided to create a rather simple simulation of planetary bodies and how their forces act on eachother. Even though the project is quite basic, the results should be rather fun to observe.

# How to Run
1. Clone GitHub Repository
2. Run requirements.txt: `pip install -r requirements.txt`
3. Open simulation.py and run file

# Dev Log

This is where I talk about what went into the simulation - thought processes, what code is where and why - essentially a good amount of waffle.

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

## Implementation

### Creating Bodies
To start, I created the constructor class for the bodies:
```python
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
```

Next, a function is needed to calcualate the distance between the current body and another:
```python
def calculateDistance(self, body: Self):
    # Calculating square distance between two bodies as a vector
    square_dist = sum(pow(elem, 2) for elem in (body.position - self.position))
    
    return square_dist
```

We also need a function for the purpose of calculating the force applied between two bodies:
```python
def calculateForce(self, body: Self, universe: Universe):
    # Calculating the force of gravity between two bodies
    force_dir = (body.position - self.position) / math.sqrt(self.calculateDistance(body))

    return (universe.GRAVITY_MULTIPLIER * force_dir * universe.GRAVITATIONAL_CONSTANT * self.mass * body.mass) / self.calculateDistance(body)
```

Now both of these have been implemented we need a function to update the velocity of the planet based on the forces being applied to it by all other planets in the universe. For this we first need to implement the universe.

### Creating Universe

The universe will mainly be constants and the array of bodies. Among the constants previously mentioned, I will also include values for a damping factor and a speed threshold for planets. This is due to the fact that once a planet has sped up in the universe, the only way for it to slow down is if another planet essentially takes the kinetic energy of that planet. This would end up leading to all planets moving incredibly fast as the simulation continued. To mitigate this, the speed of the planet can be capped and everytime the planet is registered with a velocity higher than the threshhold, the velocity will be multiplied by the damping factor to reduce it.

```python
def __init__(self, g_const, g_multiplier, colour, size, damping_factor):
    # UNIVERSAL CONSTANTS
    self.GRAVITATIONAL_CONSTANT = g_const
    self.GRAVITY_MULTIPLIER = g_multiplier
    self.UNVIERSE_COLOUR = colour
    self.DAMPING_FACTOR = damping_factor
    self.SPEED_THRESHHOLD = 3

    # Array of bodies in the universe
    self.bodies = []
    self.size = size

def add_bodies(self, bodies: list[Body]):
    # Adding bodies to the array of all bodies
    self.bodies += bodies
```

### Updating Planet Velocities
To update the planet's velocity in realtime per tick, we need to calculate the force applied to the planet by every other planet in the universe. This force vector can then be divided by the mass of the planet to get acceleration as:

$$
Force = Mass \times Acceleration \\ \therefore Acceleration = \frac{Force}{Mass}
$$

Once we have this we can use the equation $v = u + at$ to get the new velocity. As we are assuming one frame is one unit of time for this simulation, we can simplify the equation to be $v = u + a$.

```python
# Calculate new position after force is applied to the planet
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
```

We also need to be able to update the actual position of the body based on the current speed:

```python
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
```

With this, we are ready to run the simulation!

## The Simulation

For the simulation, we need to be able to generate planets with random attributes to add to the universe. This is done rather easily with a generator function:

```python
# Generates random bodies
def random_body_generator(index):
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = random.randint(0, universe.size[0])
    y = random.randint(0, universe.size[1])
    name = f"Body {index}"
    mass = random.randint(10, 200)
    initial_velocity = ((random.random()-0.5)*2, (random.random()-0.5)*2)

    return Body(x, y, name, colour, mass, initial_velocity)
```

We can then use this to generate a certain number of bodies and add them to the universe:

```python
# Generating random planets and adding them to the universe
universe.add_bodies([random_body_generator(i) for i in range(num_planets)])
```

Now we have this, all that is left to do is run the simulation loop which will loop through all bodies every tick, updating their velocities then updating their positions and drawing them onto the screen:

```python
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

    # Limit the frame rate to the frame rate of the screen
    clock.tick(165)
```

With this, we have the basic simulation done! From here I would want to either go straight to a 3D simulation or make this one slightly more advanced with body-body collisions. Currently I am leaning towards more advanced mechanics as a 3D simulation - while more interesting - is a pratically identical implementation with 3-D vectors rather than 2.

Big thanks to Sebastian Lague for being such an inspiration - check his YouTube channel out if you haven't already! [text](https://www.youtube.com/@SebastianLague)

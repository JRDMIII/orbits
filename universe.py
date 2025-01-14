class Universe:
    def __init__(self, g_const, g_multiplier, colour, size, damping_factor):
        self.GRAVITATIONAL_CONSTANT = g_const
        self.GRAVITY_MULTIPLIER = g_multiplier
        self.UNVIERSE_COLOUR = colour
        self.DAMPING_FACTOR = damping_factor
        self.SPEED_THRESHHOLD = 3
        self.bodies = []
        self.size = size
    
    def add_bodies(self, bodies):
        self.bodies += bodies
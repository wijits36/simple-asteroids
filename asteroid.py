import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_KINDS, ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    @property
    def score_value(self):
        # Smaller asteroids are worth more: large=1, medium=2, small=3
        tier = round(self.radius / ASTEROID_MIN_RADIUS)  # 3, 2, or 1
        return ASTEROID_KINDS - tier + 1

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # Create a new random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1_velocity = self.velocity.rotate(random_angle)
        asteroid_2_velocity = self.velocity.rotate(-random_angle)

        # Scale the velocity by 1.2 to give the split asteroids some momentum
        asteroid_1.velocity = asteroid_1_velocity * 1.2
        asteroid_2.velocity = asteroid_2_velocity * 1.2

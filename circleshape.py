import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple  # Populated at runtime; declared here to satisfy the type checker

    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # type: ignore  # stubs don't accept tuple of groups, but pygame handles it fine at runtime

        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius: float = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius

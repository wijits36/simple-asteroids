import pygame

from circleshape import CircleShape
from constants import (
    CONTROLLER_DPAD_DOWN,
    CONTROLLER_DPAD_LEFT,
    CONTROLLER_DPAD_RIGHT,
    CONTROLLER_DPAD_UP,
    CONTROLLER_SHOOT_AXIS,
    CONTROLLER_SHOOT_AXIS_THRESHOLD,
    CONTROLLER_SHOOT_BUTTON,
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    STICK_DEADZONE,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)  # type: ignore - Vector2 is valid at runtime but not in pygame's type stubs

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        shoot = False

        # Keyboard
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            shoot = True

        # Controller (DualSense / gamepad)
        if self.joystick is None and pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)

        if self.joystick is not None:
            num_axes = self.joystick.get_numaxes()
            num_buttons = self.joystick.get_numbuttons()

            # D-pad (button-based, e.g. DualSense on Mac)
            if num_buttons > CONTROLLER_DPAD_RIGHT:
                if self.joystick.get_button(CONTROLLER_DPAD_LEFT):
                    self.rotate(-dt)
                if self.joystick.get_button(CONTROLLER_DPAD_RIGHT):
                    self.rotate(dt)
                if self.joystick.get_button(CONTROLLER_DPAD_UP):
                    self.move(dt)
                if self.joystick.get_button(CONTROLLER_DPAD_DOWN):
                    self.move(-dt)

            # D-pad (hat-based, e.g. Xbox / Switch Pro)
            if self.joystick.get_numhats() > 0:
                hat = self.joystick.get_hat(0)
                if hat[0] == -1:
                    self.rotate(-dt)
                elif hat[0] == 1:
                    self.rotate(dt)
                if hat[1] == 1:
                    self.move(dt)
                elif hat[1] == -1:
                    self.move(-dt)

            # Left analog stick (axis 0 = x, axis 1 = y)
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)
            if abs(axis_x) > STICK_DEADZONE:
                self.rotate(axis_x * dt)
            if abs(axis_y) > STICK_DEADZONE:
                self.move(-axis_y * dt)  # axis_y is inverted: up = negative

            # Shoot: button or trigger
            trigger_pressed = (
                num_axes > CONTROLLER_SHOOT_AXIS
                and self.joystick.get_axis(CONTROLLER_SHOOT_AXIS)
                > CONTROLLER_SHOOT_AXIS_THRESHOLD
            )
            if self.joystick.get_button(CONTROLLER_SHOOT_BUTTON) or trigger_pressed:
                shoot = True

        if shoot:
            self.shoot()

        self.shot_cooldown_timer -= dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return

        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

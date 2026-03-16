import sys
from pathlib import Path

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot

HIGHSCORE_FILE = Path(__file__).parent / "highscore.txt"


def load_high_score():
    try:
        return int(HIGHSCORE_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    HIGHSCORE_FILE.write_text(str(score))


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Game init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    score = 0
    high_score = load_high_score()

    # Player init
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Asteroids init
    Asteroid.containers = (asteroids, updatable, drawable)

    # Asteroid field init
    AsteroidField.containers = updatable  # type: ignore  # stubs don't accept tuple of groups, but pygame handles it fine at runtime
    AsteroidField()

    # Shots init
    Shot.containers = (shots, updatable, drawable)

    # Game loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                print("Quitting game")
                return

        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += asteroid.score_value
                    if score > high_score:
                        high_score = score

            if asteroid.collides_with(player):
                log_event("player_hit")
                save_high_score(high_score)
                print(f"Game over! Score: {score}  High score: {high_score}")
                sys.exit()

        for sprite in drawable:
            sprite.draw(screen)

        score_surf = font.render(f"Score: {score}", True, "white")
        high_score_surf = font.render(f"Best: {high_score}", True, "grey")
        screen.blit(score_surf, (10, 10))
        screen.blit(high_score_surf, (10, 40))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()

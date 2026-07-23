import pygame
from core.state_manager import StateManager
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from states.overworld import OverworldState

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

manager = StateManager()
manager.switch(OverworldState(manager), map_name="starting_town")

running = True
while running:
    dt = clock.tick(FPS) / 1000  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            manager.handle_event(event)

    manager.update(dt)
    manager.draw(screen)
    pygame.display.flip()

pygame.quit()
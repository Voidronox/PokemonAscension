import pygame
from core.state_manager import State
from core.settings import COLOR_MENU_PANEL


class MenuState(State):
    def enter(self, **kwargs):
        print("[Menu] opened")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.manager.pop()  # return to whatever was underneath (overworld)

    def draw(self, surface):
        # drawn on top of whatever's underneath — don't fill the whole
        # surface, or the overworld behind it disappears
        panel = pygame.Rect(50, 50, 200, 300)
        pygame.draw.rect(surface, COLOR_MENU_PANEL, panel)
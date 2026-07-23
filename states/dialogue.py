import pygame
from core.state_manager import State
from core.settings import COLOR_DIALOGUE_BOX


class DialogueState(State):
    def enter(self, **kwargs):
        self.lines = kwargs.get("lines", [])
        self.index = 0
        print(f"[Dialogue] started, {len(self.lines)} lines")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.index += 1
            if self.index >= len(self.lines):
                self.manager.pop()

    def draw(self, surface):
        box = pygame.Rect(0, 400, 800, 150)
        pygame.draw.rect(surface, COLOR_DIALOGUE_BOX, box)
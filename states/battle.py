import pygame
from core.state_manager import State
from core.settings import COLOR_BATTLE_BG


class BattleState(State):
    def enter(self, **kwargs):
        self.enemy = kwargs.get("enemy")
        print(f"[Battle] started vs {self.enemy}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # temporary test exit — replace with real win/loss/flee handling
            from states.overworld import OverworldState
            self.manager.switch(OverworldState(self.manager))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(COLOR_BATTLE_BG)

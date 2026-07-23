import pygame
from core.state_manager import State
from core.settings import COLOR_OVERWORLD_BG


class OverworldState(State):
    def enter(self, **kwargs):
        # kwargs might carry e.g. which map + spawn point to load
        self.map_name = kwargs.get("map_name", "starting_town")
        print(f"[Overworld] entered: {self.map_name}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # temporary test trigger — replace with real encounter logic
                from states.battle import BattleState
                self.manager.switch(BattleState(self.manager), enemy="wild_pokemon")
            elif event.key == pygame.K_m:
                from states.menu import MenuState
                self.manager.push(MenuState(self.manager))

    def update(self, dt):
        pass  # player movement, NPC logic, tile collision go here

    def draw(self, surface):
        surface.fill(COLOR_OVERWORLD_BG)  # placeholder until tilemap rendering exists
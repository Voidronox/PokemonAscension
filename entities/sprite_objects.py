import pygame
from core.settings import TILE_SIZE

class Player:
    def __init__(self, x, y):
        # x, y are world pixel coordinates (top-left of player's tile)
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.moving = False
        self.move_progress = 0  # 0 to 1, how far through the current tile-move
        self.move_speed = 6  # tiles per second while moving
        self.direction = "down"  # for sprite facing

        self.start_x = x
        self.start_y = y
        self.target_x = x
        self.target_y = y

    def try_move(self, dx, dy, collision_rects):
        """dx, dy are -1/0/1 — one tile step in a direction."""
        if self.moving:
            return  # don't accept new input mid-move (classic Pokemon behavior)

        self.direction = self._direction_from_delta(dx, dy)

        target_x = self.x + dx * TILE_SIZE
        target_y = self.y + dy * TILE_SIZE
        future_rect = pygame.Rect(target_x, target_y, self.width, self.height)

        if any(future_rect.colliderect(r) for r in collision_rects):
            return  # blocked, don't start moving

        self.start_x, self.start_y = self.x, self.y
        self.target_x, self.target_y = target_x, target_y
        self.moving = True
        self.move_progress = 0

    def update(self, dt):
        if not self.moving:
            return
        self.move_progress += self.move_speed * dt
        if self.move_progress >= 1:
            self.x, self.y = self.target_x, self.target_y
            self.moving = False
            self.move_progress = 0
        else:
            self.x = self.start_x + (self.target_x - self.start_x) * self.move_progress
            self.y = self.start_y + (self.target_y - self.start_y) * self.move_progress

    @property
    def tile_pos(self):
        return (round(self.x / TILE_SIZE), round(self.y / TILE_SIZE))

    def _direction_from_delta(self, dx, dy):
        if dx == 1: return "right"
        if dx == -1: return "left"
        if dy == 1: return "down"
        if dy == -1: return "up"
        return self.direction

    def draw(self, surface, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        pygame.draw.rect(surface, (255, 255, 255), (screen_x, screen_y, self.width, self.height))  # placeholder

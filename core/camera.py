class Camera:
    def __init__(self, screen_w, screen_h):
        self.x = 0
        self.y = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update(self, dt, target):
        self.x = target.x - self.screen_w // 2
        self.y = target.y - self.screen_h // 2

    def apply(self, world_x, world_y):
        return world_x - self.x, world_y - self.y
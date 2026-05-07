import math
import random


class Fragment:
    def __init__(self, x, y, vx, vy, size):
        self.x    = x
        self.y    = y
        self.vx   = vx
        self.vy   = vy
        self.size = size
        self.settled = False


class ExplosionPhysics:
    """
    Single body explodes into N fragments.
    v2 of each fragment is derived from the explosion force and direction.
    Momentum is distributed evenly across fragments with random variation.
    """
    GRAVITY           = 420.0
    FLOOR_RESTITUTION = 0.48
    WALL_RESTITUTION  = 0.58
    FRICTION          = 0.78

    def __init__(self, cx, cy, force, n_fragments, floor_y,
                 border_left=0, border_right=800):
        self.floor_y      = floor_y
        self.border_left  = border_left
        self.border_right = border_right
        self.fragments    = []

        for i in range(n_fragments):
            angle = (2 * math.pi * i / n_fragments) + random.uniform(-0.25, 0.25)
            v     = force * random.uniform(0.6, 1.4)
            vx    = math.cos(angle) * v
            vy    = math.sin(angle) * v - force * 0.3   # slight upward bias
            size  = random.uniform(10, 24)
            self.fragments.append(Fragment(cx, cy, vx, vy, size))

    def update(self, dt):
        for f in self.fragments:
            if f.settled:
                continue
            f.vy += self.GRAVITY * dt
            f.x  += f.vx * dt
            f.y  += f.vy * dt

            # Floor
            if f.y + f.size / 2 >= self.floor_y:
                f.y   = self.floor_y - f.size / 2
                f.vy *= -self.FLOOR_RESTITUTION
                f.vx *= self.FRICTION
                if abs(f.vy) < 10:
                    f.vy = 0
                if abs(f.vx) < 1.5 and f.vy == 0:
                    f.settled = True

            # Walls
            if f.x - f.size / 2 <= self.border_left:
                f.x  = self.border_left + f.size / 2
                f.vx = abs(f.vx) * self.WALL_RESTITUTION
            elif f.x + f.size / 2 >= self.border_right:
                f.x  = self.border_right - f.size / 2
                f.vx = -abs(f.vx) * self.WALL_RESTITUTION

    @property
    def all_settled(self):
        return all(f.settled for f in self.fragments)

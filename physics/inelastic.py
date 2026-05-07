class InelasticPhysics:
    def __init__(self, p1, p2, v1, v2, s1, s2, m1, m2,
                 border_left, border_right, border_top, border_bottom):
        self.p1 = p1
        self.v1 = v1
        self.s1 = s1
        self.m1 = m1
        self.p2 = p2
        self.v2 = v2
        self.s2 = s2
        self.m2 = m2
        self.border_left   = border_left
        self.border_right  = border_right
        self.border_top    = border_top
        self.border_bottom = border_bottom
        self.stuck = False

    def update(self, dt):
        if not self.stuck and self.check_collision() and (self.v1 > self.v2):
            self.resolve_inelastic_impact()

        self.apply_movement(dt)
        self.clamp_borders()

    def check_collision(self):
        return (self.p1 + self.s1 >= self.p2) and (self.p1 <= self.p2 + self.s2)

    def clamp_borders(self):
        if self.p1 <= self.border_left:
            self.p1 = self.border_left
            self.v1 = abs(self.v1)
        elif self.p1 + self.s1 >= self.border_right:
            self.p1 = self.border_right - self.s1
            self.v1 = -abs(self.v1)

        if not self.stuck:
            if self.p2 <= self.border_left:
                self.p2 = self.border_left
                self.v2 = abs(self.v2)
            elif self.p2 + self.s2 >= self.border_right:
                self.p2 = self.border_right - self.s2
                self.v2 = -abs(self.v2)

    def resolve_inelastic_impact(self):
        # Objects merge — common velocity from momentum conservation
        v_common = (self.m1 * self.v1 + self.m2 * self.v2) / (self.m1 + self.m2)
        self.v1  = v_common
        self.v2  = v_common
        self.stuck = True

    def apply_movement(self, dt):
        self.p1 += self.v1 * dt
        if self.stuck:
            self.p2 = self.p1 + self.s1
        else:
            self.p2 += self.v2 * dt

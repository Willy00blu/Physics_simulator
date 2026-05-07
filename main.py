import tkinter as tk

from windows.home                    import HomeWindow
from windows.params_elastic_collision  import ElasticCollisionParams
from windows.sim_elastic_collision     import ElasticCollisionSim
from windows.params_inelastic_collision import InelasticCollisionParams
from windows.sim_inelastic_collision   import InelasticCollisionSim
from windows.params_real_collision     import RealCollisionParams
from windows.sim_real_collision        import RealCollisionSim
from windows.params_explosion          import ExplosionParams
from windows.sim_explosion             import ExplosionSim


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Simulator")
        self.resizable(False, False)
        self._current = None
        self.show_home()

    def _switch(self, new_screen):
        if self._current:
            self._current.destroy()
        self._current = new_screen
        self._current.pack()

    # ------------------------------------------------------------------ Home

    def show_home(self):
        self._switch(HomeWindow(master=self, callbacks={
            "elastic":   self.open_elastic_params,
            "inelastic": self.open_inelastic_params,
            "real":      self.open_real_params,
            "explosion": self.open_explosion_params,
        }))

    # ------------------------------------------------------------------ Elastic Collision

    def open_elastic_params(self):
        self._switch(ElasticCollisionParams(
            master=self, on_start=self.start_elastic, on_back=self.show_home
        ))

    def start_elastic(self, shape, v1, v2, s1, s2, m1, m2):
        self._switch(ElasticCollisionSim(
            self, shape, v1, v2, s1, s2, m1, m2, on_back=self.show_home
        ))

    # ------------------------------------------------------------------ Inelastic Collision

    def open_inelastic_params(self):
        self._switch(InelasticCollisionParams(
            master=self, on_start=self.start_inelastic, on_back=self.show_home
        ))

    def start_inelastic(self, shape, v1, v2, s1, s2, m1, m2):
        self._switch(InelasticCollisionSim(
            self, shape, v1, v2, s1, s2, m1, m2, on_back=self.show_home
        ))

    # ------------------------------------------------------------------ Real Collision

    def open_real_params(self):
        self._switch(RealCollisionParams(
            master=self, on_start=self.start_real, on_back=self.show_home
        ))

    def start_real(self, shape, v1, v2, s1, s2, m1, m2, e):
        self._switch(RealCollisionSim(
            self, shape, v1, v2, s1, s2, m1, m2, e, on_back=self.show_home
        ))

    # ------------------------------------------------------------------ Explosion

    def open_explosion_params(self):
        self._switch(ExplosionParams(
            master=self, on_start=self.start_explosion, on_back=self.show_home
        ))

    def start_explosion(self, shape, force, n_fragments):
        self._switch(ExplosionSim(
            self, shape, force, n_fragments, on_back=self.show_home
        ))


if __name__ == "__main__":
    app = App()
    app.mainloop()

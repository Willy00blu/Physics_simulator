import tkinter as tk
from physics.elastic import ElasticPhysics

CY = 300  # vertical center of canvas


class ElasticCollisionSim(tk.Frame):
    def __init__(self, master, shape, v1, v2, s1, s2, m1, m2, on_back=None):
        super().__init__(master)
        self.shape   = shape
        self.s1      = s1
        self.s2      = s2
        self.on_back = on_back
        self.loop_id = None
        self.p1      = 50
        self.p2      = 650

        self._create_canvas()
        self._create_objects()
        self._create_ui()

        self.engine = ElasticPhysics(
            self.p1, self.p2, v1, v2, s1, s2, m1, m2,
            border_left=0, border_right=800, border_top=0, border_bottom=600
        )
        self._update()

    def _create_canvas(self):
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()

    def _create_objects(self):
        self.obj1 = self._draw(self.p1, self.s1, "blue")
        self.obj2 = self._draw(self.p2, self.s2, "red")

    def _draw(self, x, size, fill):
        hs = size / 2
        if self.shape == "circle":
            return self.canvas.create_oval(x, CY-hs, x+size, CY+hs, fill=fill, outline="")
        else:
            return self.canvas.create_rectangle(x, CY-hs, x+size, CY+hs, fill=fill, outline="")

    def _move(self, obj_id, x, size):
        hs = size / 2
        self.canvas.coords(obj_id, x, CY-hs, x+size, CY+hs)

    def _create_ui(self):
        tk.Button(self, text="← Back to Menu", command=self._back).pack()

    def _update(self):
        self.engine.update(0.05)
        self._move(self.obj1, self.engine.p1, self.s1)
        self._move(self.obj2, self.engine.p2, self.s2)
        self.loop_id = self.after(50, self._update)

    def _back(self):
        if self.loop_id:
            self.after_cancel(self.loop_id)
            self.loop_id = None
        self.on_back()

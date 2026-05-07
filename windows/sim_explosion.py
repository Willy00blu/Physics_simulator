import tkinter as tk
from physics.explosion import ExplosionPhysics

BG       = "#07071a"
FLOOR_Y  = 530
FRAGMENT_COLOR = "#aaaacc"

COUNTDOWN_COLORS = {
    3: ("#0a0a55", "#2222bb"),
    2: ("#0a0a55", "#2222bb"),
    1: ("#0a0a55", "#2222bb"),
}


class ExplosionSim(tk.Frame):
    CX       = 400
    CY       = 265
    OBJ_SIZE = 62

    def __init__(self, master, shape, force, n_fragments, on_back=None):
        super().__init__(master, bg=BG)
        self.shape     = shape
        self.on_back   = on_back
        self.loop_id   = None
        self.phase     = "countdown"
        self.countdown = 3
        self.fragment_ids  = []
        self.flash_id      = None
        self.flash_count   = 0
        self.shockwave_id  = None
        self.shockwave_r   = 0
        self.completed     = False

        self.canvas = tk.Canvas(self, width=800, height=600, bg=BG, highlightthickness=0)
        self.canvas.pack()

        self._create_background()
        self._create_floor()
        self._create_main_object()
        self._create_ui()

        self.engine = ExplosionPhysics(
            self.CX, self.CY, force, n_fragments, floor_y=FLOOR_Y
        )
        self._start_countdown()

    # ---------------------------------------------------------------- background

    def _create_background(self):
        self.canvas.create_rectangle(0, 0, 800, FLOOR_Y, fill="#0d0d1e", outline="")

    def _create_floor(self):
        self.canvas.create_rectangle(0, FLOOR_Y, 800, 600, fill="#0c0c28", outline="")
        self.canvas.create_line(0, FLOOR_Y, 800, FLOOR_Y, fill="#5050aa", width=2)
        for x in range(0, 801, 40):
            self.canvas.create_line(x, FLOOR_Y, x, 600, fill="#111133", width=1)
        for y in range(FLOOR_Y + 30, 601, 30):
            self.canvas.create_line(0, y, 800, y, fill="#111133", width=1)

    # ---------------------------------------------------------------- main object

    def _create_main_object(self):
        cx, cy, s = self.CX, self.CY, self.OBJ_SIZE
        self.glow_outer    = self._draw(cx, cy, s + 34, "#0a0a55")
        self.glow_inner    = self._draw(cx, cy, s + 14, "#2222aa")
        self.main_obj      = self._draw(cx, cy, s, "#ffffff", outline="#aaaaff", width=1)
        self.countdown_txt = self.canvas.create_text(
            cx, cy - s // 2 - 52,
            text="3", fill="#5577ff", font=("Arial", 44, "bold")
        )

    def _draw(self, x, y, size, fill, outline="", width=0):
        s = size / 2
        if self.shape == "circle":
            return self.canvas.create_oval(x-s, y-s, x+s, y+s,
                                           fill=fill, outline=outline, width=width)
        else:
            return self.canvas.create_rectangle(x-s, y-s, x+s, y+s,
                                                fill=fill, outline=outline, width=width)

    def _move_fragment(self, fid, x, y, size):
        s = size / 2
        self.canvas.coords(fid, x-s, y-s, x+s, y+s)

    # ---------------------------------------------------------------- UI

    def _create_ui(self):
        ui = tk.Frame(self, bg=BG)
        ui.pack(fill="x", pady=3)
        tk.Button(ui, text="← Menu", command=self._back,
                  bg="#10103a", fg="#9999bb", relief="flat",
                  activebackground="#1a1a50", activeforeground="white",
                  padx=12, pady=4, font=("Arial", 10)).pack(side="left", padx=8)

    # ---------------------------------------------------------------- countdown

    def _start_countdown(self):
        if self.countdown > 0:
            self.canvas.itemconfig(self.countdown_txt,
                                   text=str(self.countdown), fill="#5577ff")
            self.countdown -= 1
            self.loop_id = self.after(1000, self._start_countdown)
        else:
            self.canvas.itemconfig(self.countdown_txt, text="")
            self.loop_id = self.after(200, self._explode)

    # ---------------------------------------------------------------- explosion

    def _explode(self):
        self.phase = "explosion"
        cx, cy = self.CX, self.CY

        for item in [self.main_obj, self.glow_inner, self.glow_outer]:
            self.canvas.delete(item)

        self.flash_id    = self.canvas.create_oval(cx-15, cy-15, cx+15, cy+15,
                                                   fill="#ffff88", outline="#ffffff", width=3)
        self.flash_count = 7
        self.shockwave_r  = 15
        self.shockwave_id = self.canvas.create_oval(
            cx-15, cy-15, cx+15, cy+15,
            outline="#ff8800", width=5, fill=""
        )

        for f in self.engine.fragments:
            fid = self._draw(f.x, f.y, f.size, FRAGMENT_COLOR)
            self.fragment_ids.append(fid)

        self.loop_id = self.after(30, self._update_loop)

    # ---------------------------------------------------------------- loop

    def _update_loop(self):
        # Flash shrinks
        if self.flash_count > 0:
            self.flash_count -= 1
            r = self.flash_count * 14
            self.canvas.coords(self.flash_id, self.CX-r, self.CY-r, self.CX+r, self.CY+r)
            if self.flash_count == 0 and self.flash_id:
                self.canvas.delete(self.flash_id)
                self.flash_id = None

        # Shockwave expands
        if self.shockwave_id:
            self.shockwave_r += 20
            r = self.shockwave_r
            self.canvas.coords(self.shockwave_id, self.CX-r, self.CY-r, self.CX+r, self.CY+r)
            w = max(1, 5 - self.shockwave_r // 35)
            self.canvas.itemconfig(self.shockwave_id, width=w)
            if self.shockwave_r >= 185:
                self.canvas.delete(self.shockwave_id)
                self.shockwave_id = None

        self.engine.update(0.03)

        for fid, f in zip(self.fragment_ids, self.engine.fragments):
            self._move_fragment(fid, f.x, f.y, f.size)

        if not self.completed and self.engine.all_settled:
            self.completed = True
            self.canvas.itemconfig(self.countdown_txt,
                                   text="SIMULATION COMPLETE", fill="#555588",
                                   font=("Arial", 14))

        self.loop_id = self.after(30, self._update_loop)

    # ---------------------------------------------------------------- cleanup

    def _back(self):
        if self.loop_id:
            self.after_cancel(self.loop_id)
            self.loop_id = None
        self.on_back()

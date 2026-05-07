import tkinter as tk

BG         = "#07071a"
PANEL_BG   = "#10103a"
FG         = "#ccccee"
ACCENT     = "#4444aa"
ACCENT_SEL = "#8888ee"


class ExplosionParams(tk.Frame):
    def __init__(self, master=None, on_start=None, on_back=None):
        super().__init__(master, bg=BG)
        self.on_start  = on_start
        self.on_back   = on_back
        self.shape     = "circle"
        self.force_var = tk.IntVar(value=260)
        self.n_var     = tk.IntVar(value=12)
        self.shape_btns = {}
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="EXPLOSION", font=("Arial", 24, "bold"),
                 bg=BG, fg=ACCENT_SEL).pack(pady=(32, 4))
        tk.Label(self, text="Configure the simulation", font=("Arial", 10),
                 bg=BG, fg="#555577").pack(pady=(0, 24))

        # Shape
        tk.Label(self, text="OBJECT SHAPE", font=("Arial", 10, "bold"),
                 bg=BG, fg=FG).pack()
        shape_row = tk.Frame(self, bg=BG)
        shape_row.pack(pady=10)
        for label, key in [("■ Square", "square"), ("⬤ Circle", "circle")]:
            lbl = tk.Label(shape_row, text=label, bg=ACCENT, fg="white",
                           relief="solid", bd=1, padx=12, pady=6,
                           cursor="hand2", font=("Arial", 11))
            lbl.bind("<Button-1>", lambda e, k=key: self._select_shape(k))
            lbl.pack(side="left", padx=6)
            self.shape_btns[key] = lbl
        self._select_shape("circle")

        # Sliders
        panel = tk.Frame(self, bg=PANEL_BG)
        panel.pack(padx=60, pady=18, fill="x")

        tk.Label(panel, text="EXPLOSION FORCE", font=("Arial", 10, "bold"),
                 bg=PANEL_BG, fg=FG).pack(pady=(14, 2))
        tk.Scale(panel, from_=80, to=520, orient=tk.HORIZONTAL,
                 variable=self.force_var, length=300,
                 bg=PANEL_BG, fg=FG, troughcolor="#1a1a4a",
                 activebackground=ACCENT_SEL, highlightthickness=0,
                 font=("Arial", 9)).pack()

        tk.Label(panel, text="FRAGMENTS COUNT", font=("Arial", 10, "bold"),
                 bg=PANEL_BG, fg=FG).pack(pady=(14, 2))
        tk.Scale(panel, from_=4, to=20, orient=tk.HORIZONTAL,
                 variable=self.n_var, length=300,
                 bg=PANEL_BG, fg=FG, troughcolor="#1a1a4a",
                 activebackground=ACCENT_SEL, highlightthickness=0,
                 font=("Arial", 9)).pack(pady=(0, 14))

        # Buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=20)
        tk.Button(btn_row, text="← Back", command=self.on_back,
                  bg="#10103a", fg=FG, relief="flat", padx=14, pady=8,
                  font=("Arial", 10), activebackground="#1a1a50").pack(side="left", padx=10)
        tk.Button(btn_row, text="  START  ▶", command=self._submit,
                  bg=ACCENT, fg="white", relief="flat", padx=14, pady=8,
                  font=("Arial", 10, "bold"), activebackground=ACCENT_SEL).pack(side="left", padx=10)

    def _select_shape(self, shape):
        self.shape = shape
        for key, lbl in self.shape_btns.items():
            lbl.config(bg=ACCENT_SEL if key == shape else ACCENT,
                       relief="sunken" if key == shape else "solid")

    def _submit(self):
        if self.on_start:
            self.on_start(self.shape, self.force_var.get(), self.n_var.get())

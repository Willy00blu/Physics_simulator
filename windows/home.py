import tkinter as tk

BG      = "#07071a"
BTN_BG  = "#10103a"
BTN_HOV = "#1a1a50"
FG      = "#ccccee"

SIMULATIONS = [
    ("ELASTIC COLLISION",   "elastic",   "#4d96ff", "Perfect conservation of kinetic energy"),
    ("INELASTIC COLLISION", "inelastic", "#6bcb77", "Objects merge together upon impact"),
    ("REAL COLLISION",      "real",      "#ffd93d", "Adjustable coefficient of restitution"),
    ("EXPLOSION",           "explosion", "#ff6b6b", "A body shatters into fragments under gravity"),
]


class HomeWindow(tk.Frame):
    def __init__(self, master=None, callbacks=None):
        super().__init__(master, bg=BG)
        self.callbacks = callbacks or {}
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="PHYSICS SIMULATOR",
                 font=("Arial", 26, "bold"), bg=BG, fg="#7777cc").pack(pady=(40, 6))
        tk.Label(self, text="Select a simulation",
                 font=("Arial", 11), bg=BG, fg="#555577").pack(pady=(0, 28))

        for name, key, color, desc in SIMULATIONS:
            self._create_entry(name, key, color, desc)

        tk.Label(self, text="", bg=BG).pack(pady=15)

    def _create_entry(self, name, key, color, desc):
        outer = tk.Frame(self, bg=BTN_BG)
        outer.pack(fill="x", padx=70, pady=5)

        tk.Frame(outer, bg=color, width=5).pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=BTN_BG)
        inner.pack(side="left", fill="both", expand=True, padx=18, pady=14)

        tk.Label(inner, text=name, font=("Arial", 12, "bold"),
                 bg=BTN_BG, fg="white", anchor="w").pack(fill="x")
        tk.Label(inner, text=desc, font=("Arial", 9),
                 bg=BTN_BG, fg="#666688", anchor="w").pack(fill="x")

        arrow = tk.Label(outer, text="▶", font=("Arial", 13),
                         bg=BTN_BG, fg=color, padx=15)
        arrow.pack(side="right")

        cb   = self.callbacks.get(key)
        all_widgets = [outer, inner, arrow] + list(inner.winfo_children())

        def on_enter(e):
            for w in all_widgets:
                w.config(bg=BTN_HOV)
        def on_leave(e):
            for w in all_widgets:
                w.config(bg=BTN_BG)
        def on_click(e):
            if cb:
                cb()

        for w in all_widgets:
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
            w.bind("<Button-1>", on_click)

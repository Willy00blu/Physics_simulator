import tkinter as tk
from tkinter import messagebox

ACCENT     = "#4444aa"
ACCENT_SEL = "#7777dd"
SIZE_MIN, SIZE_MAX = 10, 130


class InelasticCollisionParams(tk.Frame):
    def __init__(self, master=None, on_start=None, on_back=None):
        super().__init__(master)
        self.v1_var = tk.DoubleVar(value=100)
        self.v2_var = tk.DoubleVar(value=-50)
        self.s1_var = tk.DoubleVar(value=50)
        self.s2_var = tk.DoubleVar(value=50)
        self.m1_var = tk.DoubleVar(value=2)
        self.m2_var = tk.DoubleVar(value=2)
        self.on_start   = on_start
        self.on_back    = on_back
        self.shape      = "square"
        self.shape_btns = {}
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="Inelastic Collision", font=("Arial", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        tk.Label(self, text="(Objects merge together upon impact)", font=("Arial", 9)).grid(row=1, columnspan=2)

        fields = [
            ("Object 1 Velocity:", self.v1_var),
            ("Object 2 Velocity:", self.v2_var),
            ("Object 1 Size:",     self.s1_var),
            ("Object 2 Size:",     self.s2_var),
            ("Object 1 Mass:",     self.m1_var),
            ("Object 2 Mass:",     self.m2_var),
        ]
        for i, (label, var) in enumerate(fields, start=2):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="e")
            tk.Entry(self, textvariable=var).grid(row=i, column=1)

        tk.Label(self, text="Shape:").grid(row=8, column=0, sticky="e", pady=(10, 0))
        shape_row = tk.Frame(self)
        shape_row.grid(row=8, column=1, sticky="w", pady=(10, 0))
        for label, key in [("■ Square", "square"), ("⬤ Circle", "circle")]:
            lbl = tk.Label(shape_row, text=label, bg=ACCENT, fg="white",
                           relief="solid", bd=1, padx=10, pady=5,
                           cursor="hand2", font=("Arial", 11))
            lbl.bind("<Button-1>", lambda e, k=key: self._select_shape(k))
            lbl.pack(side="left", padx=4)
            self.shape_btns[key] = lbl
        self._select_shape("square")

        tk.Button(self, text="Back",  command=self.on_back).grid(row=9, column=0, pady=12)
        tk.Button(self, text="Start", command=self._submit).grid(row=9, column=1, pady=12)

    def _select_shape(self, shape):
        self.shape = shape
        for key, lbl in self.shape_btns.items():
            lbl.config(bg=ACCENT_SEL if key == shape else ACCENT,
                       relief="sunken" if key == shape else "solid")

    def _validate(self):
        s1, s2 = self.s1_var.get(), self.s2_var.get()
        m1, m2 = self.m1_var.get(), self.m2_var.get()
        if not (SIZE_MIN <= s1 <= SIZE_MAX) or not (SIZE_MIN <= s2 <= SIZE_MAX):
            messagebox.showerror("Invalid Input", f"Size must be between {SIZE_MIN} and {SIZE_MAX}")
            return False
        if m1 <= 0 or m2 <= 0:
            messagebox.showerror("Invalid Input", "Mass must be greater than 0")
            return False
        return True

    def _submit(self):
        if self.on_start and self._validate():
            self.on_start(self.shape,
                          self.v1_var.get(), self.v2_var.get(),
                          self.s1_var.get(), self.s2_var.get(),
                          self.m1_var.get(), self.m2_var.get())

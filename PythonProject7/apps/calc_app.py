# apps/calc_app.py – простой калькулятор
import tkinter as tk


class CalcApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Калькулятор")
        self.geometry("260x360")
        self.configure(bg="#050814")

        self.expr = tk.StringVar(value="0")

        entry = tk.Entry(self, textvariable=self.expr,
                         font=("Segoe UI", 18),
                         bg="#020617", fg="#e5ecff",
                         bd=0, justify="right",
                         insertbackground="#e5ecff")
        entry.pack(fill="x", padx=8, pady=8, ipady=8)

        grid = tk.Frame(self, bg="#050814")
        grid.pack(fill="both", expand=True, padx=8, pady=8)

        buttons = [
            "7 8 9 /",
            "4 5 6 *",
            "1 2 3 -",
            "0 . = +"
        ]
        for r, row in enumerate(buttons):
            for c, ch in enumerate(row.split()):
                b = tk.Button(grid, text=ch,
                              font=("Segoe UI", 14),
                              bg="#111827", fg="#e5ecff",
                              bd=0,
                              activebackground="#1f2937",
                              command=lambda x=ch: self.on_press(x))
                b.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
        for i in range(4):
            grid.grid_columnconfigure(i, weight=1)
        for i in range(4):
            grid.grid_rowconfigure(i, weight=1)

    def on_press(self, ch):
        if ch == "=":
            try:
                value = eval(self.expr.get())
                self.expr.set(str(value))
            except Exception:
                self.expr.set("Ошибка")
        else:
            if self.expr.get() == "0" and ch not in ".*/-+":
                self.expr.set(ch)
            else:
                self.expr.set(self.expr.get() + ch)

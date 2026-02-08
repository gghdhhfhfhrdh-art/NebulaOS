# fake_os.py – ядро и рабочий стол
import tkinter as tk
from tkinter import ttk, messagebox
import time
from pathlib import Path

APP_ROOT = Path(__file__).parent

from apps.explorer_app import ExplorerApp
from apps.notepad_app import NotepadApp
from apps.calc_app import CalcApp
from apps.terminal_app import TerminalApp
from apps.settings_app import SettingsApp


class FakeOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows 12 FakeOS")
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#0b0f1a")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.desktop = tk.Frame(self.root, bg="#0b0f1a")
        self.desktop.grid(row=0, column=0, sticky="nsew")
        self.taskbar = tk.Frame(self.root, bg="#11141f", height=48)
        self.taskbar.grid(row=1, column=0, sticky="ew")
        self.taskbar.grid_propagate(False)

        self.windows = []

        self.build_desktop()
        self.build_taskbar()
        self.build_start_menu()

        self.root.bind("<Escape>", lambda e: self.exit_prompt())

    # ---------- UI ----------
    def build_desktop(self):
        for r in range(3):
            self.desktop.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.desktop.grid_columnconfigure(c, weight=1)

        icons = [
            ("Проводник", "🖥️", self.open_explorer),
            ("Документы", "📁", self.open_docs),
            ("Блокнот", "📝", self.open_notepad),
            ("Калькулятор", "🧮", self.open_calc),
            ("Терминал", "⌨️", self.open_terminal),
            ("Настройки", "⚙️", self.open_settings),
        ]

        for i, (name, icon, cmd) in enumerate(icons):
            r, c = divmod(i, 4)
            cell = tk.Frame(self.desktop, bg="#0b0f1a")
            cell.grid(row=r, column=c, sticky="nw", padx=32, pady=32)
            card = tk.Frame(cell, bg="#151a28", bd=0, highlightthickness=1)
            card.config(highlightbackground="#2f5bff", highlightcolor="#2f5bff")
            card.pack(padx=6, pady=6)

            lbl_icon = tk.Label(card, text=icon,
                                font=("Segoe UI Emoji", 28),
                                bg="#151a28", fg="#e5ecff")
            lbl_icon.pack(padx=14, pady=(10, 0))
            btn = tk.Button(card, text=name,
                            font=("Segoe UI", 9),
                            fg="#cfd5ff", bg="#151a28",
                            bd=0,
                            activebackground="#20263a",
                            activeforeground="#ffffff",
                            command=cmd)
            btn.pack(padx=14, pady=(2, 10))

    def build_taskbar(self):
        self.taskbar.grid_columnconfigure(0, weight=1)
        self.taskbar.grid_columnconfigure(1, weight=1)
        self.taskbar.grid_columnconfigure(2, weight=1)

        left = tk.Frame(self.taskbar, bg="#11141f")
        center = tk.Frame(self.taskbar, bg="#11141f")
        right = tk.Frame(self.taskbar, bg="#11141f")
        left.grid(row=0, column=0, sticky="w", padx=12)
        center.grid(row=0, column=1)
        right.grid(row=0, column=2, sticky="e", padx=12)

        self.btn_start = tk.Button(center, text="⊞",
                                   font=("Segoe UI", 15, "bold"),
                                   bg="#2563eb", fg="white",
                                   activebackground="#3b82f6",
                                   bd=0, width=3,
                                   command=self.toggle_start)
        self.btn_start.pack(pady=4)

        tk.Button(left, text="📝", font=("Segoe UI Emoji", 15),
                  bg="#11141f", fg="#e5ecff", bd=0,
                  activebackground="#1b2135",
                  command=self.open_notepad).pack(side="left", padx=4)
        tk.Button(left, text="🧮", font=("Segoe UI Emoji", 15),
                  bg="#11141f", fg="#e5ecff", bd=0,
                  activebackground="#1b2135",
                  command=self.open_calc).pack(side="left", padx=4)
        tk.Button(left, text="⌨️", font=("Segoe UI Emoji", 15),
                  bg="#11141f", fg="#e5ecff", bd=0,
                  activebackground="#1b2135",
                  command=self.open_terminal).pack(side="left", padx=4)

        self.clock_label = tk.Label(right, bg="#11141f",
                                    fg="#e5ecff",
                                    font=("Segoe UI", 10))
        self.clock_label.pack()
        self.update_clock()

    def build_start_menu(self):
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.overrideredirect(True)
        self.start_menu.configure(bg="#090d18")
        self.start_menu.withdraw()

        header = tk.Frame(self.start_menu, bg="#090d18")
        header.pack(fill="x", pady=(8, 4))
        tk.Label(header, text="Windows 12 FakeOS",
                 font=("Segoe UI", 15, "bold"),
                 bg="#090d18", fg="#e5ecff").pack(anchor="w", padx=16)
        tk.Label(header, text="Пуск",
                 font=("Segoe UI", 9),
                 bg="#090d18", fg="#7f8bff").pack(anchor="w", padx=16)

        body = tk.Frame(self.start_menu, bg="#090d18")
        body.pack(fill="both", expand=True, padx=12, pady=8)

        items = [
            ("Проводник", self.open_explorer),
            ("Документы", self.open_docs),
            ("Блокнот", self.open_notepad),
            ("Калькулятор", self.open_calc),
            ("Терминал", self.open_terminal),
            ("Настройки", self.open_settings),
            ("Выход из пранка", self.exit_prompt),
        ]
        for text, cmd in items:
            b = tk.Button(body, text=text,
                          font=("Segoe UI", 10),
                          bg="#141827", fg="#dde3ff",
                          activebackground="#1c2235",
                          activeforeground="#ffffff",
                          bd=0, padx=10, pady=4,
                          anchor="w", command=cmd)
            b.pack(fill="x", pady=2)

    def toggle_start(self):
        if self.start_menu.state() == "withdrawn":
            w, h = 380, 380
            x = (self.screen_w - w) // 2
            y = self.screen_h - h - 70
            self.start_menu.geometry(f"{w}x{h}+{x}+{y}")
            self.start_menu.deiconify()
            self.start_menu.lift()
        else:
            self.start_menu.withdraw()

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M   %d.%m.%Y"))
        self.root.after(1000, self.update_clock)

    def exit_prompt(self):
        if messagebox.askyesno("Завершение", "Выключить Windows 12 FakeOS?"):
            self.root.destroy()

    # ---------- менеджер окон ----------
    def register_window(self, win):
        self.windows.append(win)
        win.protocol("WM_DELETE_WINDOW",
                     lambda w=win: self.close_window(w))

    def close_window(self, win):
        if win in self.windows:
            self.windows.remove(win)
        win.destroy()

    # ---------- запуск приложений ----------
    def open_explorer(self):
        win = ExplorerApp(self.root)
        self.register_window(win)

    def open_docs(self):
        win = ExplorerApp(self.root, start_path="/Документы")
        self.register_window(win)

    def open_notepad(self, path=None):
        win = NotepadApp(self.root, path)
        self.register_window(win)

    def open_calc(self):
        win = CalcApp(self.root)
        self.register_window(win)

    def open_terminal(self):
        win = TerminalApp(self.root, self)
        self.register_window(win)

    def open_settings(self):
        win = SettingsApp(self.root)
        self.register_window(win)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    os = FakeOS()
    os.run()

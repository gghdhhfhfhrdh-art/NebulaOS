# apps/settings_app.py – простые настройки
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

APP_ROOT = Path(__file__).parent.parent
CONFIG_PATH = APP_ROOT / "config.json"


def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"theme": "dark", "user": "User"}


def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                           encoding="utf-8")


class SettingsApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Параметры")
        self.geometry("500x300")
        self.configure(bg="#050814")

        self.cfg = load_config()

        tk.Label(self, text="Параметры Windows 12 FakeOS",
                 font=("Segoe UI", 12, "bold"),
                 bg="#050814", fg="#e5ecff").pack(anchor="w",
                                                 padx=10, pady=8)

        frame = tk.Frame(self, bg="#050814")
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        tk.Label(frame, text="Имя пользователя:",
                 bg="#050814", fg="#cfd5ff").grid(row=0, column=0,
                                                  sticky="w", pady=4)
        self.user_var = tk.StringVar(value=self.cfg.get("user", "User"))
        tk.Entry(frame, textvariable=self.user_var,
                 bg="#111827", fg="#e5ecff",
                 bd=0, insertbackground="#e5ecff").grid(row=0, column=1,
                                                       sticky="ew", pady=4)

        tk.Label(frame, text="Тема:",
                 bg="#050814", fg="#cfd5ff").grid(row=1, column=0,
                                                  sticky="w", pady=4)
        self.theme_var = tk.StringVar(value=self.cfg.get("theme", "dark"))
        ttk.Radiobutton(frame, text="Тёмная",
                        variable=self.theme_var,
                        value="dark").grid(row=1, column=1,
                                           sticky="w")
        ttk.Radiobutton(frame, text="Светлая",
                        variable=self.theme_var,
                        value="light").grid(row=2, column=1,
                                            sticky="w")

        frame.grid_columnconfigure(1, weight=1)

        tk.Button(self, text="Сохранить",
                  command=self.save).pack(anchor="e",
                                          padx=10, pady=10)

    def save(self):
        self.cfg["user"] = self.user_var.get().strip() or "User"
        self.cfg["theme"] = self.theme_var.get()
        save_config(self.cfg)
        messagebox.showinfo("Параметры", "Настройки сохранены.\n(визуальная тема пока не меняется автоматически)")

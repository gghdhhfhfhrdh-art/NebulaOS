# apps/terminal_app.py – простой терминал с командами
import tkinter as tk
from vfs import list_dir, read_file


class TerminalApp(tk.Toplevel):
    def __init__(self, master, os_core):
        super().__init__(master)
        self.title("Терминал")
        self.geometry("800x400")
        self.configure(bg="#020617")

        self.os_core = os_core
        self.cwd = "/"

        self.text = tk.Text(self, font=("Consolas", 11),
                            bg="#020617", fg="#22c55e",
                            insertbackground="#22c55e")
        self.text.pack(fill="both", expand=True)
        self.text.bind("<Return>", self.on_enter)

        self.write(f"Windows 12 FakeOS Terminal\nВведите help для списка команд.\n\n")
        self.show_prompt()

    def write(self, s):
        self.text.insert("end", s)
        self.text.see("end")

    def show_prompt(self):
        self.write(f"{self.cwd}> ")

    def on_enter(self, event):
        line = self.text.get("insert linestart", "insert lineend")
        cmd = line.split("> ", 1)[-1].strip()
        self.text.insert("end", "\n")
        self.handle_command(cmd)
        self.show_prompt()
        return "break"

    def handle_command(self, cmd):
        if not cmd:
            return
        parts = cmd.split()
        name = parts[0]

        if name == "help":
            self.write("Команды: help, dir, type <файл>, clear, run notepad, run explorer\n")
        elif name == "dir":
            items = list_dir(self.cwd)
            for it in items:
                self.write(f"{it['type']:4} {it['name']}\n")
        elif name == "type" and len(parts) > 1:
            full = self.cwd.rstrip("/") + "/" + parts[1]
            self.write(read_file(full) + "\n")
        elif name == "clear":
            self.text.delete("1.0", "end")
        elif name == "run" and len(parts) > 1:
            if parts[1] == "notepad":
                from apps.notepad_app import NotepadApp
                NotepadApp(self, None)
            elif parts[1] == "explorer":
                from apps.explorer_app import ExplorerApp
                ExplorerApp(self, "/")
            else:
                self.write("Неизвестное приложение.\n")
        else:
            self.write("Неизвестная команда. help для помощи.\n")

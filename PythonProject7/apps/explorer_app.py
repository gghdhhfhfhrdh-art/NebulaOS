# apps/explorer_app.py – проводник поверх vfs
import tkinter as tk
from tkinter import ttk, messagebox
from vfs import list_dir, create_dir, read_file
from pathlib import Path


class ExplorerApp(tk.Toplevel):
    def __init__(self, master, start_path="/"):
        super().__init__(master)
        self.title("Проводник")
        self.geometry("900x600")
        self.configure(bg="#050814")

        self.current_path = start_path

        top = tk.Frame(self, bg="#050814")
        top.pack(fill="x", padx=8, pady=4)
        tk.Label(top, text="Путь:",
                 bg="#050814", fg="#e5ecff",
                 font=("Segoe UI", 9)).pack(side="left")
        self.path_var = tk.StringVar(value=self.current_path)
        self.entry_path = tk.Entry(top, textvariable=self.path_var,
                                   bg="#111827", fg="#e5ecff",
                                   bd=0, insertbackground="#e5ecff")
        self.entry_path.pack(side="left", fill="x", expand=True, padx=4)
        tk.Button(top, text="Перейти",
                  command=self.goto_path).pack(side="left", padx=4)

        main = tk.Frame(self, bg="#050814")
        main.pack(fill="both", expand=True, padx=8, pady=4)

        self.tree = ttk.Treeview(main, show="headings",
                                 columns=("name", "type"))
        self.tree.heading("name", text="Имя")
        self.tree.heading("type", text="Тип")
        self.tree.column("name", width=300)
        self.tree.column("type", width=80)
        self.tree.pack(fill="both", expand=True, side="left")

        self.tree.bind("<Double-1>", self.on_open_selected)

        scrollbar = ttk.Scrollbar(main, orient="vertical",
                                  command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        bottom = tk.Frame(self, bg="#050814")
        bottom.pack(fill="x", padx=8, pady=4)
        tk.Button(bottom, text="Новая папка",
                  command=self.new_folder).pack(side="left")
        tk.Button(bottom, text="Открыть в блокноте",
                  command=self.open_in_notepad).pack(side="left", padx=4)

        self.reload()

    def goto_path(self):
        path = self.path_var.get().strip()
        if not path:
            path = "/"
        self.current_path = path
        self.reload()

    def reload(self):
        self.tree.delete(*self.tree.get_children())
        items = list_dir(self.current_path)
        for item in items:
            t = "Папка" if item["type"] == "dir" else "Файл"
            self.tree.insert("", "end", values=(item["name"], t))

    def resolve_selected_path(self):
        sel = self.tree.selection()
        if not sel:
            return None
        name, t = self.tree.item(sel[0], "values")
        if self.current_path in ("", "/"):
            return f"/{name}"
        return f"{self.current_path}/{name}"

    def on_open_selected(self, event):
        full = self.resolve_selected_path()
        if not full:
            return
        # если это папка
        for item in list_dir(self.current_path):
            if full.endswith(item["name"]) and item["type"] == "dir":
                self.current_path = full
                self.path_var.set(self.current_path)
                self.reload()
                return
        # файл – покажем содержимое
        content = read_file(full)
        messagebox.showinfo("Файл", f"{full}\n\n{content[:500]}")

    def new_folder(self):
        import simpledialog
        name = simpledialog.askstring("Новая папка", "Имя папки:",
                                      parent=self)
        if not name:
            return
        create_dir(self.current_path, name)
        self.reload()

    def open_in_notepad(self):
        full = self.resolve_selected_path()
        if not full:
            return
        from apps.notepad_app import NotepadApp
        NotepadApp(self, full)

# apps/notepad_app.py – блокнот поверх vfs
import tkinter as tk
from tkinter import messagebox
from vfs import read_file, write_file


class NotepadApp(tk.Toplevel):
    def __init__(self, master, path=None):
        super().__init__(master)
        self.title("Блокнот")
        self.geometry("800x500")
        self.configure(bg="#050814")

        self.file_path = path  # путь в виртуальной ФС

        top = tk.Frame(self, bg="#050814")
        top.pack(fill="x", padx=6, pady=4)
        self.lbl_path = tk.Label(top, text=self.file_path or "(новый файл)",
                                 bg="#050814", fg="#e5ecff",
                                 font=("Segoe UI", 9))
        self.lbl_path.pack(side="left")
        tk.Button(top, text="Сохранить",
                  command=self.save).pack(side="right")

        self.text = tk.Text(self, font=("Consolas", 11),
                            bg="#050814", fg="#e5ecff",
                            insertbackground="#2563eb")
        self.text.pack(fill="both", expand=True, padx=6, pady=6)

        if self.file_path:
            self.text.insert("1.0", read_file(self.file_path))
        else:
            self.text.insert("1.0",
                             "Новый файл FakeOS.\nВведите текст и нажмите Сохранить.")

    def save(self):
        if not self.file_path:
            import tkinter.simpledialog as sd
            name = sd.askstring("Сохранить в Документы",
                                "Имя файла (без пути):", parent=self)
            if not name:
                return
            self.file_path = f"/Документы/{name}"
            self.lbl_path.config(text=self.file_path)
        content = self.text.get("1.0", "end-1c")
        write_file(self.file_path, content)
        messagebox.showinfo("Сохранено",
                            f"Файл сохранён в виртуальную ФС как {self.file_path}")

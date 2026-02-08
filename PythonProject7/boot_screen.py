# boot_screen.py – NEON CINEMATIC BOOT v2
import tkinter as tk
from tkinter import ttk, messagebox
import time
import math
import random
import subprocess
from pathlib import Path

APP_ROOT = Path(__file__).parent


class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows 12 Neon Boot")
        self.root.configure(bg="#010208")
        self.root.overrideredirect(True)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_w}x{self.screen_h}+0+0")

        self.canvas = tk.Canvas(self.root, bg="#010208",
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        # длительность ~45 секунд
        self.total_ms = 45000
        self.start_ms = int(time.time() * 1000)

        # слои эффектов
        self.gradient_id = None
        self.particles = []
        self.scan_lines = []
        self.core_items = []
        self.extra_rings = []
        self.flare_items = []
        self.log_lines = []

        # градиент
        self.draw_gradient_background()

        # логотип‑ядро
        self.core_radius = 80
        self.build_core_logo()

        # текст
        self.title_text = self.canvas.create_text(
            self.screen_w // 2, self.screen_h // 2 - 140,
            text="WINDOWS 12",
            font=("Segoe UI", 34, "bold"),
            fill="#f5f7ff"
        )
        self.subtitle_text = self.canvas.create_text(
            self.screen_w // 2, self.screen_h // 2 - 100,
            text="NEON SYSTEM CORE",
            font=("Segoe UI", 12),
            fill="#b3c1ff"
        )
        self.status_text = self.canvas.create_text(
            self.screen_w // 2, self.screen_h // 2 + 110,
            text="Инициализация ядра...",
            font=("Segoe UI", 11),
            fill="#9fb4ff"
        )

        # прогресс
        self.progress = ttk.Progressbar(self.root, mode="determinate",
                                        length=self.screen_w // 3)
        self.progress.place(x=self.screen_w // 2 - self.screen_w // 6,
                            y=self.screen_h // 2 + 140)

        # эффекты
        self.create_particles(80)
        self.create_scan_lines(25)
        self.create_extra_rings()
        self.create_flares()

        self.status_phrases = [
            "Подключение к квантовой шине...",
            "Синхронизация виртуальных мониторов...",
            "Инъекция шуточных модулей...",
            "Калибровка неонового интерфейса...",
            "Ускорение потоков реальности...",
            "Оптимизация пользовательского мозга...",
            "Загрузка окружения Windows 12..."
        ]

        self.animate()
        self.animate_log_stream()
        self.root.bind("<Escape>", lambda e: self.skip_and_launch())

    # ---------- ГРАДИЕНТНЫЙ ФОН ----------
    def draw_gradient_background(self):
        # вертикальный градиент от тёмно‑синего к фиолетовому
        w, h = self.screen_w, self.screen_h
        steps = 80
        for i in range(steps):
            ratio = i / steps
            r = int(5 + 30 * ratio)
            g = int(10 + 10 * ratio)
            b = int(40 + 120 * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(h * ratio)
            y2 = int(h * (ratio + 1 / steps))
            self.canvas.create_rectangle(
                0, y1, w, y2,
                outline="", fill=color
            )

    # ---------- ЛОГОТИП‑ЯДРО И КОЛЬЦА ----------
    def build_core_logo(self):
        cx, cy = self.screen_w // 2, self.screen_h // 2
        inner = self.canvas.create_oval(
            cx - self.core_radius, cy - self.core_radius,
            cx + self.core_radius, cy + self.core_radius,
            outline="#17ffd0", width=3
        )
        self.core_items.append(inner)

        outer = self.canvas.create_oval(
            cx - self.core_radius * 1.6, cy - self.core_radius * 1.6,
            cx + self.core_radius * 1.6, cy + self.core_radius * 1.6,
            outline="#1f5fff", width=2
        )
        self.core_items.append(outer)

        for angle in range(0, 360, 45):
            r1 = self.core_radius * 1.6
            r2 = self.core_radius * 2.0
            x1 = cx + r1 * math.cos(math.radians(angle))
            y1 = cy + r1 * math.sin(math.radians(angle))
            x2 = cx + r2 * math.cos(math.radians(angle))
            y2 = cy + r2 * math.sin(math.radians(angle))
            seg = self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#3b82f6", width=1
            )
            self.core_items.append(seg)

    def create_extra_rings(self):
        cx, cy = self.screen_w // 2, self.screen_h // 2
        # несколько дополнительных колец, которые будем пульсировать
        for k in (2.3, 2.8, 3.3):
            r = self.core_radius * k
            ring = self.canvas.create_oval(
                cx - r, cy - r,
                cx + r, cy + r,
                outline="#111827", width=1
            )
            self.extra_rings.append({"id": ring, "base_r": r})

    def create_flares(self):
        # вспышки как короткие лучи вокруг ядра
        cx, cy = self.screen_w // 2, self.screen_h // 2
        for _ in range(12):
            angle = random.uniform(0, 360)
            length = random.uniform(self.core_radius * 1.2,
                                    self.core_radius * 2.5)
            line = self.canvas.create_line(
                cx, cy, cx, cy,
                fill="#f97316", width=2
            )
            self.flare_items.append({
                "id": line,
                "angle": angle,
                "length": length,
                "phase": random.uniform(0, 2 * math.pi)
            })

    # ---------- ЧАСТИЦЫ И СКАН‑ЛИНИИ ----------
    def create_particles(self, count):
        for _ in range(count):
            x = random.randint(0, self.screen_w)
            y = random.randint(0, self.screen_h)
            r = random.randint(1, 3)
            speed = random.uniform(0.3, 1.5)
            color = random.choice(["#1f5fff", "#17ffd0", "#a855ff"])
            item = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline=""
            )
            self.particles.append(
                {"id": item, "x": x, "y": y, "r": r, "speed": speed}
            )

    def create_scan_lines(self, count):
        for _ in range(count):
            y = random.randint(0, self.screen_h)
            item = self.canvas.create_line(
                0, y, self.screen_w, y,
                fill="#050816"
            )
            speed = random.uniform(0.5, 1.5)
            self.scan_lines.append({"id": item, "y": y, "speed": speed})

    def move_particles(self):
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < -10:
                p["y"] = self.screen_h + 10
                p["x"] = random.randint(0, self.screen_w)
            self.canvas.coords(
                p["id"],
                p["x"] - p["r"], p["y"] - p["r"],
                p["x"] + p["r"], p["y"] + p["r"]
            )

    def move_scan_lines(self):
        for s in self.scan_lines:
            s["y"] -= s["speed"]
            if s["y"] < 0:
                s["y"] = self.screen_h
            self.canvas.coords(s["id"],
                               0, s["y"], self.screen_w, s["y"])

    # ---------- АНИМАЦИЯ ЛОГОТИПА, КОЛЕЦ И ВСПЫШЕК ----------
    def animate_core(self, ratio):
        cx, cy = self.screen_w // 2, self.screen_h // 2
        angle = ratio * 720
        base_r = self.core_radius
        pulsed_r = base_r * (1 + 0.08 * math.sin(ratio * 14))

        # внутренний круг
        self.canvas.coords(
            self.core_items[0],
            cx - pulsed_r, cy - pulsed_r,
            cx + pulsed_r, cy + pulsed_r
        )

        # внешний круг
        outer_r = pulsed_r * 1.6
        self.canvas.coords(
            self.core_items[1],
            cx - outer_r, cy - outer_r,
            cx + outer_r, cy + outer_r
        )

        # радиальные линии
        idx = 2
        for base_angle in range(0, 360, 45):
            a = base_angle + angle
            r1 = outer_r
            r2 = outer_r * 1.25
            x1 = cx + r1 * math.cos(math.radians(a))
            y1 = cy + r1 * math.sin(math.radians(a))
            x2 = cx + r2 * math.cos(math.radians(a))
            y2 = cy + r2 * math.sin(math.radians(a))
            self.canvas.coords(self.core_items[idx], x1, y1, x2, y2)
            idx += 1

        # дополнительные кольца – мягкий пульс и цвет
        for i, ring in enumerate(self.extra_rings):
            phase = ratio * 6 + i
            scale = 1 + 0.15 * math.sin(phase)
            r = ring["base_r"] * scale
            self.canvas.coords(
                ring["id"],
                cx - r, cy - r,
                cx + r, cy + r
            )
            color = "#111827" if math.sin(phase) < 0 else "#1e293b"
            self.canvas.itemconfig(ring["id"], outline=color)

        # вспышки – лучи с меняющейся длиной и цветом
        for flare in self.flare_items:
            phase = flare["phase"] + ratio * 10
            k = (math.sin(phase) + 1) / 2  # 0..1
            length = flare["length"] * (0.6 + 0.4 * k)
            angle_rad = math.radians(flare["angle"])
            x2 = cx + length * math.cos(angle_rad)
            y2 = cy + length * math.sin(angle_rad)
            alpha_color = "#f97316" if k > 0.5 else "#fb923c"
            self.canvas.coords(flare["id"], cx, cy, x2, y2)
            self.canvas.itemconfig(flare["id"], fill=alpha_color)

    def update_texts(self, ratio):
        idx = int(ratio * len(self.status_phrases))
        idx = min(idx, len(self.status_phrases) - 1)
        self.canvas.itemconfig(self.status_text,
                               text=self.status_phrases[idx])

    # ---------- ЛОГ‑СТРИП ----------
    def animate_log_stream(self):
        now = int(time.time() * 1000)
        ratio = min((now - self.start_ms) / self.total_ms, 1.0)

        base_msgs = [
            "[CORE] Loading subsystem: VISUAL_SHELL",
            "[CORE] Mounting virtual drives...",
            "[CORE] Injecting prank modules...",
            "[SEC ] Fake antivirus signature base loaded.",
            "[SYS ] Referencing user profile: PLAYER_ONE",
            "[AI  ] Enabling sarcasm engine...",
            "[NET ] Connecting to imaginary server...",
            "[DBG ] All errors successfully ignored.",
        ]
        msg = random.choice(base_msgs)
        self.log_lines.append(msg)
        if len(self.log_lines) > 6:
            self.log_lines.pop(0)

        x1, y1 = 40, self.screen_h - 150
        x2, y2 = self.screen_w - 40, self.screen_h - 40
        self.canvas.delete("logbox")
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#020617", outline="#111827",
            tags="logbox"
        )
        for i, line in enumerate(self.log_lines):
            self.canvas.create_text(
                x1 + 16, y1 + 24 + i * 18,
                text=line,
                font=("Consolas", 9),
                fill="#93c5fd",
                anchor="w",
                tags="logbox"
            )

        if ratio < 1.0:
            self.root.after(500, self.animate_log_stream)

    # ---------- ГЛАВНЫЙ ЦИКЛ ----------
    def animate(self):
        now = int(time.time() * 1000)
        elapsed = now - self.start_ms
        ratio = min(elapsed / self.total_ms, 1.0)

        self.move_particles()
        self.move_scan_lines()
        self.animate_core(ratio)
        self.update_texts(ratio)

        self.progress["value"] = ratio * 100

        if ratio >= 1.0:
            self.launch_fake_os()
        else:
            self.root.after(33, self.animate)  # ~30 FPS

    # ---------- ЗАПУСК ОС ----------
    def launch_fake_os(self):
        self.root.destroy()
        fake_os_path = APP_ROOT / "fake_os.py"
        if fake_os_path.exists():
            subprocess.Popen(["python", str(fake_os_path)])
        else:
            messagebox.showerror(
                "Ошибка",
                f"Не найден {fake_os_path.name}. "
                f"Положи boot_screen.py и fake_os.py в одну папку."
            )

    def skip_and_launch(self):
        self.start_ms = 0
        self.total_ms = 1

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BootScreen()
    app.run()

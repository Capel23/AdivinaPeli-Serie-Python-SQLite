import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.db import get_conn, save_score
from src.game import GameSession
import random

TOTAL_POINTS = 30
TOTAL_ROUNDS = 10
HINT_COST = 2
POINTS_BONUS_ROUND = 2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Adivina la película/serie")
        self.geometry("800x600")
        self.configure(bg="#f5f5f5")
        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(self.main_frame, text="Adivina la película/serie", font=("Helvetica", 28, "bold"), bg="#f5f5f5")
        title.pack(pady=50)

        btn_play = tk.Button(self.main_frame, text="Jugar", font=("Helvetica", 16, "bold"),
                             bg="#ffd700", fg="black", command=self.start_game)
        btn_play.pack(pady=20, ipadx=20, ipady=10)

        btn_scores = tk.Button(self.main_frame, text="Ver puntuaciones", font=("Helvetica", 14),
                               bg="#ff6347", fg="white", command=self.show_scores)
        btn_scores.pack(pady=10, ipadx=20, ipady=10)

    def start_game(self):
        player_name = simpledialog.askstring("Nombre", "Introduce tu nombre:", parent=self)
        if not player_name:
            messagebox.showwarning("Atención", "Debes introducir un nombre para jugar.", parent=self)
            return

        # Obtener todas las películas/series y barajar
        items = self.get_all_items()
        if not items:
            messagebox.showwarning("Sin datos", "No hay películas o series en la base de datos.", parent=self)
            return
        random.shuffle(items)
        items = items[:TOTAL_ROUNDS]

        GameWindow(self, player_name, items, TOTAL_POINTS)

    def get_all_items(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()
        conn.close()
        return list(rows)

    def show_scores(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Puntuaciones", "No hay puntuaciones todavía.", parent=self)
            return

        scores_text = "Jugador\tPuntos\tFecha\n" + "-"*40 + "\n"
        for r in rows:
            scores_text += f"{r['player_name']}\t{r['score']}\t{r['date']}\n"

        messagebox.showinfo("Mejores puntuaciones", scores_text, parent=self)


class GameWindow(tk.Toplevel):
    def __init__(self, master, player_name, items, total_points):
        super().__init__(master)
        self.title("Juego")
        self.geometry("900x650")
        self.configure(bg="#e6f0ff")

        self.player_name = player_name
        self.items = items
        self.total_points = total_points
        self.current_index = 0
        self.current_session = None
        self.current_hints = []

        self.create_widgets()
        self.next_item()

    def create_widgets(self):
        self.lbl_round = tk.Label(self, text="", font=("Helvetica", 16, "bold"), bg="#e6f0ff")
        self.lbl_round.pack(pady=10)

        self.lbl_masked = tk.Label(self, text="", font=("Courier", 32, "bold"), bg="#e6f0ff")
        self.lbl_masked.pack(pady=20)

        self.points_var = tk.DoubleVar()
        self.progress_points = ttk.Progressbar(self, maximum=TOTAL_POINTS, variable=self.points_var, length=500)
        self.progress_points.pack(pady=10)

        self.lbl_points = tk.Label(self, text=f"Puntos: {self.total_points}", font=("Helvetica", 14), bg="#e6f0ff")
        self.lbl_points.pack()

        self.frame_hints = tk.Frame(self, bg="#e6f0ff")
        self.frame_hints.pack(pady=15, fill=tk.X, padx=50)

        self.btn_guess = tk.Button(self, text="Adivinar", font=("Helvetica", 16, "bold"),
                                   bg="#32cd32", fg="white", command=self.adivinar)
        self.btn_guess.pack(pady=15, ipadx=20, ipady=10)

    def next_item(self):
        if self.total_points <= 0:
            messagebox.showinfo("Game Over", "¡Has perdido todos tus puntos!", parent=self)
            self.destroy()
            return

        if self.current_index >= len(self.items):
            messagebox.showinfo("Fin del juego", f"¡Has terminado!\nPuntos finales: {self.total_points}", parent=self)
            save_score(self.player_name, self.total_points)
            self.destroy()
            return

        self.item = self.items[self.current_index]
        self.current_index += 1

        self.current_session = GameSession(self.item)
        self.current_hints = self.get_hints(self.item["id"])
        random.shuffle(self.current_hints)

        self.update_labels()
        self.populate_hints()

    def get_hints(self, item_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hints WHERE item_id = ?", (item_id,))
        rows = cur.fetchall()
        conn.close()
        return list(rows)

    def update_labels(self):
        self.lbl_masked.config(text=self.current_session.mask_title())
        self.lbl_round.config(text=f"Ronda {self.current_index} / {len(self.items)}")
        self.points_var.set(self.total_points)
        self.lbl_points.config(text=f"Puntos: {self.total_points}")

    def populate_hints(self):
        for widget in self.frame_hints.winfo_children():
            widget.destroy()

        for idx, hint in enumerate(self.current_hints):
            btn = tk.Button(self.frame_hints, text=f"Pista {idx+1} (-{HINT_COST} pts)",
                            font=("Helvetica", 12), bg="#ffa500", fg="black",
                            command=lambda h=hint: self.usar_pista(h))
            btn.pack(pady=5, ipadx=10, ipady=5, fill=tk.X)

    def usar_pista(self, hint):
        messagebox.showinfo("Pista", hint["text"], parent=self)
        self.total_points -= HINT_COST
        if self.total_points <= 0:
            messagebox.showinfo("Game Over", "¡Has perdido todos tus puntos!", parent=self)
            self.destroy()
            return
        self.current_hints.remove(hint)
        self.populate_hints()
        self.update_labels()

    def adivinar(self):
        guess = simpledialog.askstring("Adivinar", "Introduce el título:", parent=self)
        if guess:
            if self.current_session.guess(guess):
                # Recuperar puntos al pasar de ronda
                self.total_points = min(TOTAL_POINTS, self.total_points + POINTS_BONUS_ROUND)
                messagebox.showinfo("¡Correcto!", f"¡Has adivinado!\n+{POINTS_BONUS_ROUND} puntos", parent=self)
                self.next_item()
            else:
                messagebox.showinfo("Incorrecto", "No es correcto.", parent=self)
                self.total_points -= 2
                if self.total_points <= 0:
                    messagebox.showinfo("Game Over", "¡Has perdido todos tus puntos!", parent=self)
                    self.destroy()
                    return
                self.update_labels()

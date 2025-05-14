import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput import mouse, keyboard

clicking = False
click_button = mouse.Button.left
click_interval = 0.01

def click_loop():
    global clicking
    mouse_controller = mouse.Controller()
    while True:
        if clicking:
            mouse_controller.click(click_button)
            time.sleep(click_interval)
        else:
            time.sleep(0.1)

def toggle_clicking():
    global clicking
    clicking = not clicking
    state = "ACTIVÉ" if clicking else "DÉSACTIVÉ"
    state_label.config(text=f"AutoClick : {state}", foreground="#66ffcc" if clicking else "#ff9999")

def set_left_click():
    global click_button
    click_button = mouse.Button.left
    status_label.config(text="Mode : Clic Gauche", foreground="#80dfff")

def set_right_click():
    global click_button
    click_button = mouse.Button.right
    status_label.config(text="Mode : Clic Droit", foreground="#ff80bf")

def update_interval():
    global click_interval
    try:
        value = float(interval_entry.get())
        click_interval = max(0.001, value)
        interval_label.config(text=f"Intervalle : {value:.3f}s", fg="#b3ff66")  # Mise à jour de l'intervalle directement ici
    except ValueError:
        interval_label.config(text="⚠ Valeur invalide", fg="#ff6666")

def on_hotkey(key):
    if key == keyboard.Key.f8:
        toggle_clicking()

def toggle_topmost():
    root.attributes('-topmost', top_var.get())

# Setup fenêtre
root = tk.Tk()
root.title("AutoClicker Neo")
root.geometry("400x470")  # Agrandissement de la fenêtre pour plus d'espace
root.resizable(False, False)

# Canvas de fond
gradient = tk.Canvas(root, width=400, height=470, highlightthickness=0)
gradient.pack(fill="both", expand=True)

def draw_gradient(canvas, color1, color2):
    for i in range(550):
        r = int(int(color1[1:3], 16) + (int(color2[1:3], 16) - int(color1[1:3], 16)) * i / 550)
        g = int(int(color1[3:5], 16) + (int(color2[3:5], 16) - int(color1[3:5], 16)) * i / 550)
        b = int(int(color1[5:7], 16) + (int(color2[5:7], 16) - int(color1[5:7], 16)) * i / 550)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 480, i, fill=color)

draw_gradient(gradient, "#100020", "#202060")

# Styles
style = ttk.Style()
style.theme_use("clam")

style.configure("Neon.TButton",
    foreground="white",
    background="#5eafff",
    padding=6,
    font=("Consolas", 10),
    relief="flat",  # Pas de relief
    highlightthickness=0,  # Pas de pointillés autour
    bd=0  # Pas de bordure
)
style.map("Neon.TButton",
    background=[("active", "#a1d8ff")]
)

style.configure("Red.TButton", background="#ff80bf", relief="flat", highlightthickness=0, bd=0)  # Pas de pointillés
style.map("Red.TButton", background=[("active", "#ffcce6")])

style.configure("Blue.TButton", background="#80dfff", relief="flat", highlightthickness=0, bd=0)  # Pas de pointillés
style.map("Blue.TButton", background=[("active", "#cceeff")])

# UI
tk.Label(root, text="🎮 AutoClicker Neo", fg="#a080ff", bg="#100020", font=("Consolas", 14, "bold"), bd=0).place(relx=0.5, y=15, anchor="n")

tk.Label(root, text="Intervalle (sec) :", bg="#100020", fg="white", font=("Consolas", 10), bd=0).place(relx=0.5, y=55, anchor="n")

# Label qui affiche l'intervalle actuel
interval_label = tk.Label(root, text=f"Intervalle : {click_interval:.3f}s", bg="#100020", fg="#b3ff66", font=("Consolas", 10), bd=0)
interval_label.place(relx=0.5, y=85, anchor="n")  # Affichage juste sous le texte

interval_entry = tk.Entry(root, font=("Consolas", 10), justify="center", bg="#1f1f2e", fg="#ffffff", insertbackground="white", relief="flat", width=12)
interval_entry.insert(0, "0.01")
interval_entry.place(relx=0.5, y=120, anchor="n")

ttk.Button(root, text="Mettre à jour l'intervalle", command=update_interval, style="Neon.TButton").place(relx=0.5, y=150, anchor="n")

ttk.Button(root, text="Mode Clic Gauche", command=set_left_click, style="Blue.TButton").place(relx=0.5, y=200, anchor="n")
ttk.Button(root, text="Mode Clic Droit", command=set_right_click, style="Red.TButton").place(relx=0.5, y=240, anchor="n")

status_label = tk.Label(root, text="Mode : Clic Gauche", bg="#100020", fg="#80dfff", font=("Consolas", 10), bd=0)
status_label.place(relx=0.5, y=280, anchor="n")

state_label = tk.Label(root, text="AutoClick : DÉSACTIVÉ", bg="#100020", fg="#ff9999", font=("Consolas", 10, "bold"), bd=0)
state_label.place(relx=0.5, y=310, anchor="n")

tk.Label(root, text="Appuie sur F8 pour activer/désactiver", bg="#100020", fg="#aaaaff", font=("Consolas", 9), bd=0).place(relx=0.5, y=350, anchor="n")

# Case à cocher pour le topmost
top_var = tk.BooleanVar(value=False)
top_check = tk.Checkbutton(root, text="Toujours au 1er plan", variable=top_var,
    command=toggle_topmost,
    bg="#100020", fg="white", selectcolor="#2a2a3a",
    font=("Consolas", 9), activebackground="#100020", activeforeground="white", relief="flat", highlightthickness=0, bd=0)  # Pas de pointillés
top_check.place(relx=0.5, y=390, anchor="n")

# Threads
click_thread = threading.Thread(target=click_loop, daemon=True)
click_thread.start()

keyboard_listener = keyboard.Listener(on_press=on_hotkey)
keyboard_listener.start()

root.mainloop()

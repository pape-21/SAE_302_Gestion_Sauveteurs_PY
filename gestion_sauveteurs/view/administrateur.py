import tkinter as tk
from tkinter import ttk

# --- Fonction : ouvrir la fenêtre "Utilisateur" ---
def ouvrir_utilisateur():
    user_win = tk.Toplevel()
    user_win.title("Utilisateur")
    user_win.geometry("300x200")

    tk.Button(user_win, text="Ajouter utilisateur", width=25).pack(pady=15)
    tk.Button(user_win, text="Supprimer utilisateur", width=25).pack(pady=15)


root = tk.Tk()
root.title("Administrateur")
root.geometry("650x250")

# --- Thème "clam" pour un tableau propre ---
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=28,
                fieldbackground="white",
                bordercolor="#9e9e9e",
                borderwidth=1)

style.configure("Treeview.Heading",
                background="#e6e6e6",
                foreground="black",
                bordercolor="#9e9e9e",
                borderwidth=1)

style.map("Treeview", background=[("selected", "#3498db")])

# --- Cadre des boutons ---
frame_buttons = tk.Frame(root)
frame_buttons.pack(side="left", padx=20, pady=20)

# ICI on connecte le bouton à la nouvelle fenêtre !
tk.Button(frame_buttons, text="Modifier les utilisateurs",
          width=25, command=ouvrir_utilisateur).pack(pady=10)

tk.Button(frame_buttons, text="Informations générales", width=25).pack(pady=10)
tk.Button(frame_buttons, text="Voir le planning", width=25).pack(pady=10)

# --- Cadre du tableau ---
frame_table = tk.Frame(root)
frame_table.pack(side="right", padx=20, pady=20)

columns = ("ID", "Nom", "Prénom", "Profil")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=1)

table.heading("ID", text="ID")
table.heading("Nom", text="Nom")
table.heading("Prénom", text="Prénom")
table.heading("Profil", text="Profil")

table.column("ID", width=50, anchor="center", stretch=False)
table.column("Nom", width=150, anchor="center", stretch=False)
table.column("Prénom", width=150, anchor="center", stretch=False)
table.column("Profil", width=120, anchor="center", stretch=False)

table.insert("", "end", values=("1", "Gueye", "Sokhna", "Admin"))

table.pack()

root.mainloop()


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Ajouter utilisateur ---
def fenetre_ajouter_utilisateur():
    win = tk.Toplevel()
    win.title("Ajouter utilisateur")
    win.geometry("300x250")

    tk.Label(win, text="Nom :").pack(pady=5)
    entry_nom = tk.Entry(win, width=30)
    entry_nom.pack()

    tk.Label(win, text="Prénom :").pack(pady=5)
    entry_prenom = tk.Entry(win, width=30)
    entry_prenom.pack()

    tk.Label(win, text="Profil :").pack(pady=5)
    entry_profil = tk.Entry(win, width=30)
    entry_profil.pack()

    tk.Button(win, text="Ajouter", width=20).pack(pady=15)


# --- Supprimer utilisateur ---
def fenetre_supprimer_utilisateur():
    win = tk.Toplevel()
    win.title("Supprimer utilisateur")
    win.geometry("300x150")

    tk.Label(win, text="ID :").pack(pady=5)
    entry_id = tk.Entry(win, width=30)
    entry_id.pack()

    def supprimer():
        user_id = entry_id.get()
        messagebox.showinfo("Supprimer", f"Utilisateur avec ID {user_id} supprimé (simulation)")

    tk.Button(win, text="Supprimer", width=20, command=supprimer).pack(pady=15)


# --- Fenêtre Utilisateur ---
def ouvrir_utilisateur():
    user_win = tk.Toplevel()
    user_win.title("Utilisateur")
    user_win.geometry("300x200")

    tk.Button(user_win, text="Ajouter utilisateur", width=25,
              command=fenetre_ajouter_utilisateur).pack(pady=15)

    tk.Button(user_win, text="Supprimer utilisateur", width=25,
              command=fenetre_supprimer_utilisateur).pack(pady=15)


# --- Fenêtre Informations générales ---
def fenetre_informations_generales():
    info_win = tk.Toplevel()
    info_win.title("Informations générales")
    info_win.geometry("500x150")

    columns = ("Nom", "Prénom", "Spécialité", "Département")
    table = ttk.Treeview(info_win, columns=columns, show="headings", height=1)

    for col in columns:
        table.heading(col, text=col)

    table.column("Nom", width=120, anchor="center", stretch=False)
    table.column("Prénom", width=120, anchor="center", stretch=False)
    table.column("Spécialité", width=130, anchor="center", stretch=False)
    table.column("Département", width=130, anchor="center", stretch=False)

    table.pack(padx=10, pady=10, fill="both", expand=True)


# --- Fenêtre Planning vide ---
def fenetre_planning():
    plan_win = tk.Toplevel()
    plan_win.title("Planning")
    plan_win.geometry("550x250")
    # Pour l'instant, la fenêtre est vide


# --- Fenêtre principale ---
root = tk.Tk()
root.title("Administrateur")
root.geometry("650x300")

# --- Thème tableau ---
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

# --- Cadre boutons ---
frame_buttons = tk.Frame(root)
frame_buttons.pack(side="left", padx=20, pady=20)

tk.Button(frame_buttons, text="Modifier les utilisateurs",
          width=25, command=ouvrir_utilisateur).pack(pady=10)
tk.Button(frame_buttons, text="Informations générales", width=25,
          command=fenetre_informations_generales).pack(pady=10)
tk.Button(frame_buttons, text="Voir le planning", width=25,
          command=fenetre_planning).pack(pady=10)

# --- Cadre tableau utilisateurs ---
frame_table = tk.Frame(root)
frame_table.pack(side="right", padx=20, pady=20)

columns = ("ID", "Nom", "Prénom", "Profil")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)

for col in columns:
    table.heading(col, text=col)

table.column("ID", width=50, anchor="center", stretch=False)
table.column("Nom", width=150, anchor="center", stretch=False)
table.column("Prénom", width=150, anchor="center", stretch=False)
table.column("Profil", width=120, anchor="center", stretch=False)

# Ligne exemple
table.insert("", "end", values=("1", "Gueye", "Sokhna", "Admin"))

table.pack(fill="both", expand=True)

# --- Lancement de l'application ---
root.mainloop()






import tkinter as tk
from tkinter import messagebox

# Fonction du bouton "Se connecter"
def se_connecter():
    user = entry_user.get()
    password = entry_pass.get()

    if user == "admin" and password == "1234":
        messagebox.showinfo("Succès", "Connexion réussie !")
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects")

# Fonction du bouton "Voir planning"
def voir_planning():
    messagebox.showinfo("Planning", "Voici votre planning (exemple).")

# Fenêtre principale
root = tk.Tk()
root.title("Application de gestion de planning")
root.geometry("350x250")

# --- Interface ---

tk.Label(root, text="Login :").pack(pady=5)
entry_user = tk.Entry(root, width=30)
entry_user.pack()

tk.Label(root, text="Mot de passe :").pack(pady=5)
entry_pass = tk.Entry(root, width=30, show="*")
entry_pass.pack()

tk.Button(root, text="Voir planning", width=20, command=voir_planning).pack(pady=10)
tk.Button(root, text="Se connecter", width=20, command=se_connecter).pack()

# Lancement de l'application
root.mainloop()

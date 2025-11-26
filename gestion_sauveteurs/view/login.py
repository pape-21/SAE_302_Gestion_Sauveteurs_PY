import tkinter as tk
from tkinter import messagebox
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

def lancer_login():
    """
    Lance la fenêtre de login et retourne le rôle de l'utilisateur connecté (ou None).
    """
    # Variable pour stocker le résultat (astuce pour le récupérer après mainloop)
    resultat_connexion = {"role": None}

    root = tk.Tk()
    root.title("Connexion - Gestion Sauveteurs")
    root.geometry("350x250")

    def se_connecter():
        identifiant = entry_user.get()
        mot_de_passe = entry_pass.get()

        crud = UtilisateurCRUD()
        role = crud.verifier_connexion(identifiant, mot_de_passe)

        if role:
            resultat_connexion["role"] = role
            root.destroy() # On ferme la fenêtre, ce qui arrête le mainloop
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # Interface
    tk.Label(root, text="Identifiant :").pack(pady=5)
    entry_user = tk.Entry(root)
    entry_user.pack(pady=5)

    tk.Label(root, text="Mot de passe :").pack(pady=5)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack(pady=5)

    tk.Button(root, text="Se connecter", command=se_connecter).pack(pady=20)

    root.mainloop() # Bloque ici tant que la fenêtre est ouverte

    # Une fois la fenêtre fermée (par success ou croix rouge), on retourne le rôle
    return resultat_connexion["role"]
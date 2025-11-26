import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

def lancer_administrateur():
    # --- Fenêtre principale ---
    root = tk.Tk()
    root.title("Espace Administrateur - Gestion des Comptes")
    root.geometry("850x500")

    # Instance du CRUD pour dialoguer avec la BDD
    crud = UtilisateurCRUD()

    # --- Fonctions Métier ---

    def rafraichir_tableau():
        """Vide le tableau et le remplit avec les données de la BDD."""
        # 1. On vide le tableau actuel
        for item in table.get_children():
            table.delete(item)
        
        # 2. On récupère les utilisateurs depuis la base
        utilisateurs = crud.get_tous()
        
        # 3. On les insère ligne par ligne
        for u in utilisateurs:
            # u est un dictionnaire grâce au row_factory dans le CRUD
            table.insert("", "end", values=(u['id'], u['identifiant'], u['role']))

    def action_ajouter():
        """Ouvre une popup pour créer un user."""
        win = tk.Toplevel()
        win.title("Nouvel Utilisateur")
        win.geometry("300x300")

        tk.Label(win, text="Identifiant :").pack(pady=5)
        entry_identifiant = tk.Entry(win)
        entry_identifiant.pack(pady=5)

        tk.Label(win, text="Mot de passe :").pack(pady=5)
        entry_mdp = tk.Entry(win, show="*") # Masqué pour sécurité
        entry_mdp.pack(pady=5)

        tk.Label(win, text="Rôle :").pack(pady=5)
        combo_role = ttk.Combobox(win, values=["administrateur", "gestionnaire", "lecture"], state="readonly")
        combo_role.current(2) # Sélection par défaut 'lecture'
        combo_role.pack(pady=5)

        def valider_ajout():
            identifiant = entry_identifiant.get()
            mdp = entry_mdp.get()
            role = combo_role.get()

            if identifiant and mdp and role:
                succes = crud.ajouter_utilisateur(identifiant, mdp, role)
                if succes:
                    messagebox.showinfo("Succès", f"Utilisateur '{identifiant}' créé.")
                    rafraichir_tableau() # Mise à jour immédiate de la liste
                    win.destroy()
                else:
                    messagebox.showerror("Erreur", "L'identifiant existe déjà ou erreur BDD.")
            else:
                messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")

        tk.Button(win, text="Valider", command=valider_ajout, bg="#4CAF50", fg="white").pack(pady=20)

    def action_supprimer():
        """Supprime la ligne sélectionnée."""
        selection = table.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur dans la liste.")
            return

        # On récupère les données de la ligne sélectionnée
        item = table.item(selection[0])
        valeurs = item['values'] 
        identifiant_cible = valeurs[1] # Colonne 1 = Identifiant

        # Sécurité : on empêche de supprimer 'admin' pour ne pas se bloquer
        if identifiant_cible == "admin":
            messagebox.showerror("Interdit", "Vous ne pouvez pas supprimer le super-admin par défaut.")
            return

        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer '{identifiant_cible}' ?"):
            succes = crud.supprimer(identifiant_cible)
            if succes:
                rafraichir_tableau()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer cet utilisateur.")

    # --- Interface Graphique ---

    # Titre
    lbl_titre = tk.Label(root, text="Gestion des Utilisateurs (Synchronisé BDD)", font=("Helvetica", 16, "bold"))
    lbl_titre.pack(pady=15)

    # Conteneur principal
    frame_contenu = tk.Frame(root)
    frame_contenu.pack(fill="both", expand=True, padx=20, pady=10)

    # Panneau Latéral (Boutons)
    frame_boutons = tk.Frame(frame_contenu)
    frame_boutons.pack(side="left", fill="y", padx=(0, 20))

    btn_style = {"width": 20, "pady": 5}
    tk.Button(frame_boutons, text="Ajouter Utilisateur", command=action_ajouter, bg="#2196F3", fg="white", **btn_style).pack(pady=10)
    tk.Button(frame_boutons, text="Supprimer Sélection", command=action_supprimer, bg="#F44336", fg="white", **btn_style).pack(pady=10)
    tk.Button(frame_boutons, text="Actualiser", command=rafraichir_tableau, **btn_style).pack(pady=10)
    tk.Frame(frame_boutons, height=50).pack() # Espaceur
    tk.Button(frame_boutons, text="Déconnexion", command=root.destroy, **btn_style).pack(side="bottom", pady=10)

    # Tableau (Treeview)
    columns = ("ID", "Identifiant", "Rôle")
    table = ttk.Treeview(frame_contenu, columns=columns, show="headings", selectmode="browse")
    
    table.heading("ID", text="ID")
    table.column("ID", width=50, anchor="center")
    
    table.heading("Identifiant", text="Identifiant")
    table.column("Identifiant", width=200, anchor="w") # w = West (aligné à gauche)
    
    table.heading("Rôle", text="Rôle")
    table.column("Rôle", width=150, anchor="center")

    # Scrollbar pour le tableau
    scrollbar = ttk.Scrollbar(frame_contenu, orient="vertical", command=table.yview)
    table.configure(yscroll=scrollbar.set)
    
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Chargement initial des données
    rafraichir_tableau()

    root.mainloop()
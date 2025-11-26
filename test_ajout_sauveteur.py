# Fichier : test_ajout_sauveteur.py
import time
# On importe la fonction magique qui fait (Insert Local + Envoi Réseau)
from gestion_sauveteurs.gestion_sauveteurs import ajouter_sauveteur

print("--- TEST SYNCHRONISATION SAUVETEUR ---")
print("1. Ajout de 'Jean Dujardin' dans la base locale...")
print("2. Envoi automatique vers les pairs...")

# Appel de la fonction du contrôleur
ajouter_sauveteur(
    nom="Dujardin", 
    prenom="Jean", 
    departement="75", 
    specialite="Plongée"
)

print("\n[OK] Commande exécutée.")
print("-> Vérifie le terminal de l'autre machine (Machine B) !")
print("-> Vérifie la base de données de l'autre machine.")
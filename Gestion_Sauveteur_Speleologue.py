"""
Point d'entrée principal (Launcher) de l'application de Gestion des Sauveteurs.

Ce script est destiné à être exécuté depuis la racine du projet. 
Il se charge d'importer et de lancer le contrôleur principal situé dans le package `gestion_sauveteurs`.

Usage:
    Exécuter la commande suivante dans le terminal :
    ``python3 Gestion_Sauveteur_Speleologue.py``
"""

import sys
import os

# On s'assure que le dossier courant est bien dans le path python
# (Utile si le script est lancé depuis un autre répertoire)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gestion_sauveteurs.gestion_sauveteurs import main as lancer_application

def main():
    """Fonction principale du script racine.
    
    Elle délègue l'exécution à la fonction :func:`gestion_sauveteurs.gestion_sauveteurs.main`.
    """
    # On lance simplement le chef d'orchestre défini dans le package
    lancer_application()

if __name__ == "__main__":
    main()
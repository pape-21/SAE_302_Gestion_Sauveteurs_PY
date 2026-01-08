.. Documentation Gestion Sauveteurs

Bienvenue dans la documentation de Gestion Sauveteurs !
=======================================================

Cette documentation détaille le fonctionnement technique de l'application SAE 302, 
des interactions réseaux à la gestion de la base de données.

.. toctree::
   :maxdepth: 2
   :caption: Table des matières:

Contrôleur Principal
--------------------

C'est le point d'entrée de l'application, qui orchestre l'interface et le réseau.

.. automodule:: gestion_sauveteurs.gestion_sauveteurs
   :members:
   :undoc-members:
   :show-inheritance:

Configuration de la Base de Données
-----------------------------------

Gestion de la connexion SQLite et de l'initialisation.

.. automodule:: gestion_sauveteurs.database
   :members:
   :undoc-members:
   :show-inheritance:

Module Réseau (Communication)
-----------------------------

Ce module gère la découverte des autres machines et l'échange de données.

Connexion et Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: gestion_sauveteurs.connexion_réseaux
   :members:
   :undoc-members:
   :show-inheritance:

Module CRUD (Données)
---------------------

Cette partie gère toutes les requêtes SQL vers la base de données.

Gestion des Sauveteurs
~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: gestion_sauveteurs.crud.sauveteur
   :members:
   :undoc-members:
   :show-inheritance:

Gestion du Planning
~~~~~~~~~~~~~~~~~~~
.. automodule:: gestion_sauveteurs.crud.planning
   :members:
   :undoc-members:
   :show-inheritance:

Gestion des Utilisateurs
~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: gestion_sauveteurs.crud.utilisateur
   :members:
   :undoc-members:
   :show-inheritance:

Lancement de l'Application
--------------------------

Script racine permettant de démarrer le logiciel.

.. automodule:: Gestion_Sauveteur_Speleologue
   :members:
   :undoc-members:
   :show-inheritance:


Indices et Tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
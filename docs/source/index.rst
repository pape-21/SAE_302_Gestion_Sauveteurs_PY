.. Application graphique de gestion des sauveteurs spéléologues documentation master file, created by
   sphinx-quickstart on Sun Oct 19 16:47:51 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Documentation Gestion Sauveteurs

Bienvenue dans la documentation de Gestion Sauveteurs !
=======================================================

Cette documentation détaille le fonctionnement technique de l'application, 
notamment les interactions avec la base de données (CRUD).

.. toctree::
   :maxdepth: 2
   :caption: Table des matières:

Module CRUD (Base de données)
-----------------------------

Cette partie gère toutes les communications avec la base de données SQLite.

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


Indices et Tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
-- Table des utilisateurs (Admin, Gestionnaire, Lecture)
CREATE TABLE IF NOT EXISTS utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifiant TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL, -- A hasher idéalement
    role TEXT CHECK(role IN ('administrateur', 'gestionnaire', 'lecture')) NOT NULL
);

-- Table des sauveteurs
CREATE TABLE IF NOT EXISTS sauveteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    departement TEXT,
    specialite TEXT NOT NULL,
    statut TEXT DEFAULT 'disponible' 
    -- statuts : disponible, approche, sous_terre, gestion, exterieur, repos, civiere
);

-- Table du planning (Lien Sauveteur <-> Créneau horaire)
-- On stocke l'état du sauveteur pour un créneau donné
CREATE TABLE IF NOT EXISTS planning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sauveteur_id INTEGER,
    heure_debut DATETIME, -- Format ISO8601 recommandé
    heure_fin DATETIME,     
    statut_mission TEXT, 
    FOREIGN KEY(sauveteur_id) REFERENCES sauveteur(id) ON DELETE CASCADE
);

-- Insertion d'un admin par défaut pour ne pas être bloqué
INSERT OR IGNORE INTO utilisateur (identifiant, mot_de_passe, role) 
VALUES ('admin', 'admin', 'administrateur');                    
-- ===========================================
-- Base de données SQLite : Gestion des sauveteurs spéléologues
-- Auteur : Pape Birame Fall
-- Date de création : 2025-10-31
-- ===========================================

-- Table des sauveteurs
CREATE TABLE sauveteurs (
    id_sauveteur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    departement TEXT,
    specialite TEXT CHECK(specialite IN (
        'communication',
        'assistance victime',
        'medicale',
        'desobstruction',
        'evacuation',
        'brancardage',
        'recherche'
     
    ))
);

-- Table des missions
CREATE TABLE missions (
    id_mission INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_mission TEXT NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME,             -- NULL si mission en cours
    lieu TEXT
);

-- Table du planning
CREATE TABLE planning (
    id_planning INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sauveteur INTEGER NOT NULL,
    id_mission INTEGER NOT NULL,
    statut TEXT CHECK(statut IN (
        'disponible',
        'approche',
        'sous_terre',
        'gestion',
        'mission_exterieure',
        'repos',
        'brancardage'
    )),
    heure_debut DATETIME NOT NULL,
    heure_fin DATETIME,            -- NULL si mission en cours
    FOREIGN KEY(id_sauveteur) REFERENCES sauveteurs(id_sauveteur),
    FOREIGN KEY(id_mission) REFERENCES missions(id_mission)
);

-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL,
    profil TEXT CHECK(profil IN (
        'gestionnaire',
        'lecture',
        'administration',
        'utilisateur'
    ))
);

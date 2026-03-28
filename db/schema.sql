-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Company Table (1-to-1 relationship with User)
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    mvp TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Experiments Table (1-to-many relationship with User)
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id TEXT,
    title TEXT,
    type TEXT,
    goal TEXT,
    channel TEXT,
    user_note TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Experiment Runs Table (1-to-many relationship with Experiment)
CREATE TABLE IF NOT EXISTS experiment_runs (
    id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    status TEXT,
    plan_json TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (experiment_id) REFERENCES experiments (id) ON DELETE CASCADE
);

-- Experiment Outputs Table (1-to-many relationship with Experiment)
CREATE TABLE IF NOT EXISTS experiment_outputs (
    id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    kind TEXT,
    label TEXT,
    content TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments (id) ON DELETE CASCADE
);

import sqlite3

DB_NAME = "SurfCaster.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'  -- default role is 'unauth'
        );
    """)
    conn.commit()   

    cursor.executescript("""
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES ('admin', 'admin123','admin@admin', 'admin');
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES ('rev', 'rev123','rev@rev', 'reviewer');
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES ('unauth', 'unauth123','unauth@unauth', 'unauth');
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES ('user', 'user123','user@user', 'user');
    """
    )
    conn.commit()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
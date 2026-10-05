import sqlite3


DATABASE = "database/dsa_mentor.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_db_connection()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS mentor_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems(id)
    )
""")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            description TEXT NOT NULL,
            examples TEXT,
            constraints TEXT
        )
    """)

    connection.commit()
    connection.close()

import sqlite3
from pathlib import Path


# Store the database inside the JARVIS project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "database" / "jarvis_memory.db"


class JarvisMemory:

    def __init__(self):
        self.create_database()

    def create_database(self):
        """Create the database and memories table if they don't exist."""

        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_memory(self, key, value):
        """Save a new memory or update an existing one."""

        key = key.strip().lower()
        value = value.strip()

        if not key or not value:
            raise ValueError("Memory key and value cannot be empty.")

        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("""
                INSERT INTO memories (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))

    def get_memory(self, key):
        """Retrieve one specific memory."""

        with sqlite3.connect(DATABASE_PATH) as connection:
            result = connection.execute(
                "SELECT value FROM memories WHERE key = ?",
                (key.strip().lower(),)
            ).fetchone()

        return result[0] if result else None

    def get_all_memories(self):
        """Retrieve all saved memories."""

        with sqlite3.connect(DATABASE_PATH) as connection:
            results = connection.execute("""
                SELECT key, value FROM memories ORDER BY key
            """).fetchall()

        return results

    def delete_memory(self, key):
        """Delete one specific memory."""

        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.execute(
                "DELETE FROM memories WHERE key = ?",
                (key.strip().lower(),)
            )

        return cursor.rowcount > 0

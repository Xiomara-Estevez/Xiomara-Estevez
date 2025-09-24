import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class DatabaseManager:
    """Handles database connections and operations."""

    def __init__(self):
        self.connection_params = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

    @contextmanager
    def get_connection(self):
        """Provide a DB connection and ensure it's closed properly."""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params, cursor_factory=RealDictCursor)
            yield conn
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and optionally fetch results.

        Always commits the transaction before returning to ensure INSERT/UPDATE
        operations persist and RETURNING values are available to callers.
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)

                if fetch == "one":
                    row = cursor.fetchone()
                    conn.commit()
                    return row
                if fetch == "all":
                    rows = cursor.fetchall()
                    conn.commit()
                    return rows

                conn.commit()
                return cursor.rowcount

    def test_connection(self):
        try:
            result = self.execute_query("SELECT version()", fetch="one")
            print("✅ Database connected successfully!")
            print(f"📊 Version: {result['version']}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False


# Module-level instance used by the app
db = DatabaseManager()
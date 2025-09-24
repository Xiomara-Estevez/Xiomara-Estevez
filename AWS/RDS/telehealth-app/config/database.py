import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables
load_dotenv()

class DatabaseManager:
    """Handles database connections and operations"""
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = psycopg2.connect(
                **self.connection_params,
                cursor_factory=RealDictCursor
            )
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and optionally fetch results"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch == 'one':
                    return cursor.fetchone()
                elif fetch == 'all':
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
    
    def test_connection(self):
        """Test database connection"""
        try:
            result = self.execute_query("SELECT version()", fetch='one')
            print(f"✅ Database connected successfully!")
            print(f"📊 Version: {result['version']}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

# IMPORTANT: Create the global db instance
db = DatabaseManager()
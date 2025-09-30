# simple_db_test.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

print("🔍 Environment variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=5432,
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"✅ Direct connection works: {version[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Direct connection failed: {e}")
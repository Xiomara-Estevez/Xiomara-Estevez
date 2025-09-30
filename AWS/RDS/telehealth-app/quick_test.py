# quick_test.py - Simple database test
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    # Test connection with your actual credentials
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    
    print("✅ Database connection successful!")
    print(f"📊 Version: {result[0]}")
    
    connection.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n🔍 Check these in your .env file:")
    print(f"DB_HOST={os.getenv('DB_HOST')}")
    print(f"DB_PORT={os.getenv('DB_PORT')}")
    print(f"DB_NAME={os.getenv('DB_NAME')}")
    print(f"DB_USER={os.getenv('DB_USER')}")
    print("DB_PASSWORD=[hidden]")
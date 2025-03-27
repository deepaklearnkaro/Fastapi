import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = =postgresql://studdb_owner:npg_ojDk0aBts1xQ@ep-black-smoke-a4l2d9e5-pooler.us-east-1.aws.neon.tech/studdb?sslmode=require

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

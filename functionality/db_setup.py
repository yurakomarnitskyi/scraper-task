import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

time.sleep(15)

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        url VARCHAR,
        title VARCHAR,
        price_usd INTEGER,
        odometer INTEGER,
        username VARCHAR,
        phone_number VARCHAR,
        image_url VARCHAR,
        images_count INTEGER,
        car_number VARCHAR,
        car_vin VARCHAR,
        datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cur.close()
conn.commit()
conn.close()

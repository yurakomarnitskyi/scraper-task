import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def dump_database():
    os.environ["PGPASSWORD"] = DB_PASSWORD  
    dump_path = f"scraper-task/dumps/db_dump_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
    subprocess.run([r"C:\Program Files\PostgreSQL\14\bin\pg_dump.exe", 
                    f"--host={DB_HOST}", f"--port={DB_PORT}", f"--username={DB_USER}",
                    f"--no-password", 
                    f"--format=plain", f"--dbname={DB_NAME}", 
                    f"--file={dump_path}"])
if __name__ == "__main__":
    dump_database()



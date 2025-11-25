import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db_config import DB_CONFIG

def ensure_database_exists():
    conn = pyodbc.connect(
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database_master']};"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{DB_CONFIG['database']}'")
    exists = cursor.fetchone()

    if not exists:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
    conn.commit()
    conn.close()

def get_engine():
    return engine

def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()

def get_connection_string():
    connection_string = (
    f"mssql+pyodbc://@{DB_CONFIG['server']}/"
    f"{DB_CONFIG['database']}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"    
    )
    return connection_string

# engine
engine = create_engine(get_connection_string(), echo=False)

# session factory
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

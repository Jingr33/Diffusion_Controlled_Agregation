import os

ENV = os.getenv("APP_ENV", "dev")

DB_CONFIG = {
    "driver": os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}"),
    "server": os.getenv("DB_SERVER", "localhost"),
    "database": os.getenv("DB_NAME", "DiffusionControlledAgregationDB"),
    "database_master": os.getenv("DB_MASTER_NAME", "master"),
    "uid": os.getenv("DB_USER", "sa"),
    "pwd": os.getenv("DB_PASS", ""),
}

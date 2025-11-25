import os

ENV = os.getenv("APP_ENV", "dev")

if ENV == "dev":
    DB_CONFIG = {
        "driver": "{ODBC Driver 17 for SQL Server}",
        "server": "LAPTOP-3BB5L61H\SQLEXPRESS",
        "database": "DiffusionControlledAgregationDB",
        "database_master": "master",
        "uid": "LAPTOP-3BB5L61H\jirka",
        "pwd": "root"
    }
else:
    DB_CONFIG = {
        "driver": "{ODBC Driver 17 for SQL Server}",
        "server": "db",
        "database": "DiffusionControlledAgregationDB",
        "database_master": "master",
        "uid": "sa",
        "pwd": "MojeHeslo123!"
    }

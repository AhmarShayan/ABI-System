from dotenv import load_dotenv
from pyodbc import connect
from sqlalchemy import create_engine
import os

load_dotenv()

def get_engine(database:str):
    server=os.environ.get("DB_SERVER","localhost\\SQLEXPRESS")
    driver=os.environ.get("DB_DRIVER","ODBC+Driver+17+for+SQL+Server")
    trusted=os.environ.get("DB_TRUSTED","yes")

    connection_string=f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection={trusted}"

    return create_engine(connection_string)


def get_db_connection(db_name:str):
    server=os.environ.get("DB_SERVER","localhost\\SQLEXPRESS")
    driver=os.environ.get("DB_DRIVER","ODBC+Driver+17+for+SQL+Server")

    conn=connect(f"Driver={driver};"
    f"Server={server};"
    f"Database={db_name};"
    "Trusted_Connection=yes;")

    return conn
from sqlalchemy import create_engine
from agents.cleaning_agent import data_cleaner
import pandas as pd
import sys


raw_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_RAW_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
clean_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_CLEAN_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

def run_cleaner(upload_id:str):
    raw_table=f"raw_data_table_{upload_id}"
    clean_table=f"clean_data_table_{upload_id}"

    try:
        print(f"Reading from {raw_table}")
        df_raw=pd.read_sql_table(raw_table,con=raw_engine)
    except Exception as e:
        raise RuntimeError(f"File coudn't be read {e}")

    try:
        print("Running the cleaning operation")
        df_clean=data_cleaner(df_raw)
    except Exception as e:
        raise RuntimeError(f"Cleaning operation failed {e}")

    try:
        print("Appending the cleaned data into database")
        df_clean.to_sql(clean_table,con=clean_engine,if_exists="replace",index=False)
    except Exception as e:
        raise RuntimeError(f"Appending operation failed {e}")
    
from fastapi import APIRouter,HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
from agents.sql_generation import generate_sql
from langchain_community.utilities import SQLDatabase
from services.query_execute import execute_query

router=APIRouter()


class QueryClass(BaseModel):
    upload_id:str
    use_clean:bool

@router.post("/dashboard/")
async def generate_sql_dashboard(payload:QueryClass):
    try:
        if payload.use_clean==True:
            db=SQLDatabase.from_uri("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_CLEAN_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            db_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_CLEAN_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            table_name=f"clean_data_table_{payload.upload_id}"

        else:
            db=SQLDatabase.from_uri("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_RAW_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            db_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_RAW_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            table_name=f"raw_data_table_{payload.upload_id}"

        final_code=generate_sql(table_name,db_engine)

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to generate the sql code {e}")
    

    try:
        print("Generating the result")
        results=execute_query(db,final_code)

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to execute the sql query")


    return results

    

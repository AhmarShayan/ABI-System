from sqlalchemy import create_engine
from fastapi import APIRouter,HTTPException
from answering_agent import data_answerer
from pydantic import BaseModel
import pandas as pd

router=APIRouter()


class QueryClass(BaseModel):
    question:str
    upload_id:str
    use_clean:bool=True

@router.post("/ask/")
async def ask_question(payload:QueryClass):
    try:
        if payload.use_clean==True:
            db_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_CLEAN_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            table_name=f"clean_data_table_{payload.upload_id}"

        else:
            db_engine=create_engine("mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_RAW_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
            table_name=f"raw_data_table_{payload.upload_id}"

        df=pd.read_sql_table(table_name=table_name,con=db_engine)

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to load table {e}")
    

    try:
        answer=data_answerer(df,payload.question)
        return {"asnwer":answer}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to answer your question {e}")
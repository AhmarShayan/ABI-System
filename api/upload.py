from fastapi import APIRouter,File,UploadFile,HTTPException
import pandas as pd
from sqlalchemy import create_engine
import io
from datetime import datetime
import uuid
from services.run_cleaning import run_cleaner
from fastapi.concurrency import run_in_threadpool

router=APIRouter()

engine=create_engine( "mssql+pyodbc://@localhost\\SQLEXPRESS/ABI_RAW_DATA?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

@router.post("/upload.csv/")
async def upload_csv(file:UploadFile=File(...)):

    if not file.filename.endswith(".csv"): # type: ignore
        raise HTTPException(status_code=400,detail="Only csv files are allowed!")
    
    
    try:
        contents=await file.read()
        df=pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error reading the file {e}")
    
    upload_id=str(uuid.uuid4()).replace("-","_")
    upload_time=datetime.now()
    table_name=f"raw_data_table_{upload_id}"

    try:
        df.to_sql(table_name,con=engine,if_exists="fail",index=False)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Failed to write to DB: {e}")
    
    try:
        print("Cleaning and uploading data")
        await run_in_threadpool(run_cleaner, upload_id)
    except Exception as e:
        print("Cleaning error:", e)
        raise HTTPException(status_code=500, detail=f"Cleaning operation failed: {e}")

    
    return {"message":"CSV uploaded to SQL Server","rows":len(df),"upload_id": upload_id,"upload_time": upload_time.isoformat()}
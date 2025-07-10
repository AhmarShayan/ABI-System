from fastapi import FastAPI
import upload
import query

app=FastAPI()

app.include_router(upload.router)
app.include_router(query.router)
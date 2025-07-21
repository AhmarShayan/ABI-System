from fastapi import FastAPI
import api.upload
import api.query
import api.dashboard_data

app=FastAPI()

app.include_router(api.upload.router)
app.include_router(api.query.router)
app.include_router(api.dashboard_data.router)

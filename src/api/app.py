from fastapi import FastAPI
from api.v1.router import api_v1_router

idp_app = FastAPI(title="Intelligent Document Processing API", version="1.0.0")
idp_app.include_router(api_v1_router)

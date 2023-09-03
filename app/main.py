from fastapi import FastAPI
import os
import sys
repo_dir = os.path.abspath(__file__).split('/app')[0]
sys.path.append(f'{repo_dir}')
from app.routers.router import router as recsys_router


app = FastAPI()
app.include_router(recsys_router)


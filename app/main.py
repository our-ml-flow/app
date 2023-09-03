from fastapi import FastAPI
from app.routers.router import router as recsys_router


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(recsys_router, prefix="/recsys", tags=["svd"])

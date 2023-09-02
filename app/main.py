from fastapi import FastAPI

from app.routers.item import router as item_router
from app.routers.nft import router as nft_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(item_router, prefix="/item", tags=["Item"])
app.include_router(nft_router, prefix="/nft", tags=["NFT"])

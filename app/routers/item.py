from fastapi import APIRouter

from app.schemas.request import RequestItem
from app.schemas.response import ResponseBody

router = APIRouter()

simple_db = {}

@router.post("/{item_id}")
async def add_item(item_id: int, item: RequestItem):
    simple_db[item_id] = item

    return {"message": "Item added"}

@router.get("/{item_id}", response_model = ResponseBody)
async def read_item(item_id: int):
    return ResponseBody(data=simple_db[item_id])
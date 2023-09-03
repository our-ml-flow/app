from fastapi import APIRouter

from app.schemas.request import RequestModel
from app.schemas.response import ResponseModel
from app.utils.utils import get_recommendations

router = APIRouter()


@router.post("/predict", response_model=ResponseModel)
def recsys(data: RequestModel):
    result = get_recommendations(data.collections)
    return ResponseModel(recommendations=result)

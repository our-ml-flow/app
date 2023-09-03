from fastapi import APIRouter
import os
import sys
repo_dir = os.path.abspath(__file__).split('/app')[0]
sys.path.append(f'{repo_dir}')

from app.schemas.request import RequestModel
from app.schemas.response import ResponseModel
from app.utils.utils import get_recommendations

router = APIRouter()


@router.post("/", response_model=ResponseModel)
def recsys(data: RequestModel):
    result = get_recommendations(data.collections)
    return ResponseModel(recommendations=result)

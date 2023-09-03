from pydantic import BaseModel
from typing import List


class ResponseModel(BaseModel): #모델 실행 후 결과값
    recommendations: List[str]
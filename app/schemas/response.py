from pydantic import BaseModel
from typing import List


class ResponseModel(BaseModel):
    recommendations: List[str]
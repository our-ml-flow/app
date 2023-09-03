from pydantic import BaseModel
from typing import List


class RequestModel(BaseModel): 
    collections: List[str]
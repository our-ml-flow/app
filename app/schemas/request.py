from pydantic import BaseModel
from typing import List


class RequestModel(BaseModel): #모델에 입력되어야 할 값은 오너 지갑주소 & 지갑 내 컬렉션. 지갑없을 경우 컬렉셔녀 리스트만
    collections: List[str]
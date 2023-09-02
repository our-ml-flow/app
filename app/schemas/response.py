from pydantic import BaseModel
from typing import List

class ResponseItem(BaseModel):
    name: str
    price: float = None
    is_offer: bool = None
    
class ResponseBody(BaseModel):
    data: ResponseItem

class ResponseNft(BaseModel):
    name: str
    count: int

class NftPrediction(BaseModel):
    prediction: List[ResponseNft]
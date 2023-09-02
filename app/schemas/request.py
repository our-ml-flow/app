from pydantic import BaseModel

class RequestItem(BaseModel):
    name: str
    price: float = None
    is_offer: bool = None

class NftFeature(BaseModel):
    feature1: str

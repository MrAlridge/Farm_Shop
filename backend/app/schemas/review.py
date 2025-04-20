from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    content: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    user_id: int
    created_at: datetime
    user: dict

    class Config:
        orm_mode = True 
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int
    is_poor_product: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    main_image: Optional[str] = None
    images: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_poor_product = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 添加多图片支持
    images = Column(JSON, default=list)  # 存储图片URL列表
    main_image = Column(String(255))  # 主图URL
    
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product") 
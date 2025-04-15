from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.product import Product
from ..models.review import Review
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..schemas.review import ReviewCreate, ReviewResponse
from ..utils.auth import get_current_user
from ..utils.upload import save_upload_file

router = APIRouter()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.get("/products", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()

@router.post("/products/{product_id}/reviews", response_model=ReviewResponse)
def create_review(
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    db_review = Review(
        **review.dict(),
        product_id=product_id,
        user_id=current_user.id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
def get_product_reviews(
    product_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    reviews = db.query(Review)\
        .filter(Review.product_id == product_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return reviews

@router.post("/products/{product_id}/images")
async def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="没有权限")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    image_urls = []
    for file in files:
        url = await save_upload_file(file)
        image_urls.append(url)
    
    if not product.main_image:
        product.main_image = image_urls[0]
    
    if not product.images:
        product.images = []
    product.images.extend(image_urls)
    
    db.commit()
    return {"message": "图片上传成功", "urls": image_urls} 
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
import re
from faker import Faker

app = FastAPI()
faker = Faker()

# 假資料生成
products = [
    {
        "id": str(i),
        "name": faker.company(),
        "description": faker.text(),
        "price": round(faker.random_number(digits=4) / 100, 2),  # 0 ~ 99.99
        "is_location_offer": faker.random_int(min=0, max=1),
        "is_rental": faker.random_int(min=0, max=1),
        "in_stock": faker.random_int(min=0, max=100),
        "brand": {
            "id": str(i),
            "name": faker.company(),
            "slug": faker.slug()
        },
        "category": {
            "id": str(i),
            "parent_id": str(i-1) if i > 0 else None,
            "name": faker.word(),
            "slug": faker.slug(),
            "sub_categories": [faker.word() for _ in range(2)]
        },
        "product_image": {
            "by_name": faker.name(),
            "by_url": faker.url(),
            "source_name": faker.company(),
            "source_url": faker.url(),
            "file_name": f"product_{i}.jpg",
            "title": faker.sentence(nb_words=3),
            "id": str(i)
        }
    }
    for i in range(1, 201)  # 200筆假資料
]

# Message 輸入資料驗證
class Message(BaseModel):
    name: str
    subject: str
    message: str
    email: EmailStr

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', v):
            raise ValueError('Name 必須是中文或英文')
        return v

    @validator('subject', 'message')
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError('Subject 和 Message 不可為空')
        return v

@app.get("/products")
def get_products(
    page: int = 1,
    between: Optional[str] = Query(None),
    sort: Optional[str] = Query(None)
):
    items_per_page = 10
    filtered_products = products

    if between:
        parts = between.split(',')
        if len(parts) == 3 and parts[0] == "price":
            try:
                min_price = float(parts[1])
                max_price = float(parts[2])
                filtered_products = [
                    p for p in filtered_products if min_price <= p['price'] <= max_price
                ]
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid between parameters")

    if sort:
        parts = sort.split(',')
        if len(parts) == 2:
            key, order = parts
            if key in ["name", "price"]:
                reverse = (order == "desc")
                filtered_products = sorted(filtered_products, key=lambda x: x.get(key, ""), reverse=reverse)

    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_products = filtered_products[start:end]

    return paginated_products

@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/messages")
def post_message(message: Message):
    return {"message": "收到訊息！", "data": message.dict()}

@app.get("/health")
def health_check():
    return {"status": "ok"}
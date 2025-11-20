from datetime import datetime

from ninja import Schema


class ProductIn(Schema):
    name: str
    description: str
    price: float
    stock: int


class ProductOut(Schema):
    id: int
    name: str
    description: str
    price: float
    stock: int


class CartIn(Schema):
    product_id: int
    quantity: int


class CartOut(Schema):
    id: int
    product_id: int
    quantity: int


class OrderOut(Schema):
    id: int
    status: str
    created_at: datetime
    total_price: float

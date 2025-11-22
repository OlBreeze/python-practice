from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()


@router.get("/products", response=List[ProductOut])
def list_products(request):
    return Product.objects.all()


@router.post("/products", response=ProductOut)
def create_product(request, payload: ProductIn):
    product = Product.objects.create(**payload.dict())
    return product


@router.get("/products/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    return get_object_or_404(Product, id=product_id)


@router.put("/products/{product_id}", response=ProductOut)
def update_product(request, product_id: int, payload: ProductIn):
    product = get_object_or_404(Product, id=product_id)
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@router.delete("/products/{product_id}")
def delete_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"success": True}


@router.post("/cart", response=CartOut)
def add_to_cart(request, payload: CartIn):
    cart = Cart.objects.create(user=request.user, **payload.dict())
    return cart


@router.delete("/cart/{cart_id}")
def remove_from_cart(request, cart_id: int):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart.delete()
    return {"success": True}


@router.post("/orders", response=OrderOut)
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart_items.delete()
    return order


@router.get("/orders", response=List[OrderOut])
def list_orders(request):
    return Order.objects.filter(user=request.user)


@router.put("/orders/{order_id}/status", response=OrderOut)
def update_order_status(request, order_id: int, status: str):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return order

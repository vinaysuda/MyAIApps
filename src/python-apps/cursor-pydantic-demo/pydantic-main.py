from pydantic import BaseModel, EmailStr


class OrderItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float


class Order(BaseModel):
    order_id: str
    email_id: EmailStr
    items: list[OrderItem]


print(Order.model_json_schema())

data = {
    "order_id": "ORD-001",
    "email_id": "test@example.com",
    "items": [
        {"product_id": "P1", "name": "Widget", "quantity": 2, "price": 29.99},
        {"product_id": "P2", "name": "Gadget", "quantity": 1, "price": 49.99},
    ],
}

# order = Order(**data)

order = Order.model_validate(data)

print(order.model_dump_json())

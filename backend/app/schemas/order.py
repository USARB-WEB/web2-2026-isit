from pydantic import BaseModel, Field

from app.schemas.order_product import OrderProductCreate


class OrderBase(BaseModel):
    client_name: str = Field(min_length=1, max_length=100)


class OrderCreate(OrderBase):
    products: list[OrderProductCreate] = Field(default_factory=list)


class OrderUpdate(OrderBase):
    pass

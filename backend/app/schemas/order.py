from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_product import OrderProductCreate, OrderProductRead


class OrderBase(BaseModel):
    client_name: str = Field(min_length=1, max_length=100)


class OrderCreate(OrderBase):
    products: list[OrderProductCreate] = Field(default_factory=list)


class OrderUpdate(OrderBase):
    pass


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    products: list[OrderProductRead] = Field(default_factory=list)
    products_count: int = 0
    total_sum: float = 0.0


class OrderSummary(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    products_count: int = 0
    total_sum: float = 0.0

from pydantic import BaseModel, ConfigDict, Field


class OrderProductBase(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    pass


class OrderProductRead(OrderProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int

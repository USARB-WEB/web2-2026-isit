from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    pass


class ProductCategoryRead(ProductCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

from pydantic import BaseModel, Field

class NutrientsOut(BaseModel):
    calories: float|None = Field(...)
    fats: float|None = Field(...)
    carbs: float|None = Field(...)
    proteins: float|None = Field(...)
    unsaturated_fats: float|None = Field(...)
    sugar: float|None = Field(...)
    salt: float|None = Field(...)
    portion: float|None = Field(...)


class ProductOut(BaseModel):  # define your model
    id: str = Field(...)
    name: str = Field(...)
    description: str | dict = Field(...)
    nutrients: NutrientsOut


class ProductsWithFieldOut(BaseModel):
    product: str = Field(...)
    field: dict = Field(...)
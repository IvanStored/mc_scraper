from fastapi import APIRouter
from fastapi.params import Depends

from misc.utils import ProductService, get_product_service
from schemas import ProductOut, ProductsWithFieldOut

products_router = APIRouter(
    prefix="/products",  tags=["products"]
)

@products_router.get("/")
async def get_all_products(service: ProductService = Depends(get_product_service)) -> list[ProductOut]:
    await service.get_all_products()
    return service.products


@products_router.get("/{query}/")
async def get_product_by_name(query: str, service: ProductService = Depends(get_product_service)) -> list[ProductOut]:
    products_list = service.find_product(query=query)
    return products_list

@products_router.get("/{query}/{field}/")
async def get_nutrition_field(query: str, field: str, service: ProductService = Depends(get_product_service)) -> list[ProductsWithFieldOut]:
    products_list = service.find_field(query=query, field=field)

    return products_list
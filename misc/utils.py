import asyncio
import http
import json
import os.path

from fastapi import HTTPException

from config import settings
from misc.scraper import run_scraper


class ProductService:

    products = None

    async def __initialize(self):
        await self.get_all_products()

    def __init__(self):
        asyncio.run(self.__initialize())

    def get_data_from_json(self) -> None:
        with open(settings.file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.products = data

    async def get_all_products(self) -> None:
        if not os.path.exists(settings.file_name):
            await run_scraper()
        self.get_data_from_json()

    def find_product(self, query: str) -> list | None:
        results = []
        for product in self.products:
            if query.lower() in product["name"].lower():
                results.append(product)
        if results:
            return results
        raise HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND,
            detail=f"Product {query} was not found",
        )

    def _get_field(self, product: dict, field: str):
        try:
            return {"name": field, "value": product["nutrients"][field]}
        except KeyError:
            raise HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail=f"Field {field} was not found",
            )

    def find_field(self, query: str, field: str):
        products_list = self.find_product(query=query)
        products_list_with_fields = [
            {
                "product": product["name"],
                "field": self._get_field(product=product, field=field),
            }
            for product in products_list
        ]
        return products_list_with_fields


def get_product_service():
    return ProductService()

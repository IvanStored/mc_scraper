import asyncio
import json

import aiohttp
import bs4
from loguru import logger

from config import settings


class ProductScraper:
    BASE_URL = "https://www.mcdonalds.com"

    def __init__(self):
        self.menu_url = f"{self.BASE_URL}/ua/uk-ua/eat/fullmenu.html"
        self.api_call = f"{self.BASE_URL}/dnaapp/itemDetails"
        self.api_params = {
            "country": "UA",
            "language": "uk",
            "showLiveData": "true",
        }
        self.product_cell = "li.cmp-category__item"
        self.output_file = settings.file_name
        self.products_data = []

    async def fetch_product_data(self, session, product_id):
        self.api_params["item"] = product_id
        try:
            async with session.get(
                url=self.api_call, params=self.api_params
            ) as res:
                product_dict = await res.json()

            product_dict = product_dict["item"]
            name = product_dict["item_name"]
            description = product_dict["description"]

            nutrient_facts = product_dict["nutrient_facts"]["nutrient"]
            nutrient_ids = {
                "calories": "energy_kcal",
                "fats": "fat",
                "carbs": "carbohydrate",
                "proteins": "protein",
                "unsaturated_fats": "НЖК",
                "sugar": "Цукор",
                "salt": "salt",
                "portion": "primary_serving_size",
            }

            def parse_nutrient_value(value):
                try:
                    return float(value)
                except ValueError:
                    logger.warning(
                        f"Non-convertible value '{value}' for product {product_id} was set to None."
                    )
                    return None

            nutrient_values = {
                key: [
                    parse_nutrient_value(item["value"])
                    for item in nutrient_facts
                    if item["nutrient_name_id"] == value
                ][0]
                for key, value in nutrient_ids.items()
            }

            product_info = {
                "id": product_id,
                "name": name,
                "description": description,
                "nutrients": nutrient_values,
            }

            self.products_data.append(product_info)
            logger.success(f"Product {product_id} was saved")
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {e}")

    async def scrape_products(self):
        tasks = []
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(url=self.menu_url) as res:
                    data = await res.text()

                    soup = bs4.BeautifulSoup(data, "html.parser")
                    products = soup.select(self.product_cell)

                    for product in products:
                        product_id = product.get("data-product-id")
                        task = asyncio.create_task(
                            self.fetch_product_data(session, product_id)
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks)
                    self.save_to_json()
        except Exception as e:
            logger.error(f"Error scraping products: {e}")

    def save_to_json(self):
        try:
            with open(self.output_file, "w") as file:
                json.dump(
                    self.products_data, file, indent=4, ensure_ascii=False
                )
            logger.success(f"Data saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving data to JSON: {e}")


async def run_scraper():
    scraper = ProductScraper()
    await scraper.scrape_products()


if __name__ == "__main__":
    asyncio.run(run_scraper())

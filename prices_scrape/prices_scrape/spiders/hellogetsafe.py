import json
import jmespath
from datetime import date
from distutils.util import strtobool

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

from prices_scrape.items import PricesScrapeItem


class HellogetsafeLoader(ItemLoader):
    default_output_processor = TakeFirst()


class HellogetsafeSpider(scrapy.Spider):
    name = 'hellogetsafe'
    allowed_domains = ['hellogetsafe.com',
                       'www.hellogetsafe.com',
                       'insurance-service.api.getsafe.eu']
    PAYLOAD = {}

    def __init__(
            self,
            zip_code='01067',
            family_coverage=False,
            drone_coverage=False,
            *a,
            **kw
    ):
        super().__init__(*a, **kw)
        self.zip_code = zip_code
        self.family_coverage = bool(strtobool(str(family_coverage)))
        self.drone_coverage = bool(strtobool(str(drone_coverage)))

        product_configurations = [
            self._get_product_config("liability_premium_basic_neodigital_de")
        ]
        if self.drone_coverage:
            product_configurations.append(
                self._get_product_config("liability_premium_drones_neodigital_de")
            )
        self.PAYLOAD = {"product_configurations": product_configurations}

    def _get_product_config(self, key):
        return {
            "product_key": key,
            "configuration_data": {
                "deductible_amount": 0,
                "family_coverage": self.family_coverage,
                "zip_code": self.zip_code,
                "number_of_claims_in_last_5y": 0
            },
            "effective_on": str(date.today())
        }

    def start_requests(self):
        yield Request(
            url='https://insurance-service.api.getsafe.eu/api/v2/markets/de/prices',
            method='POST',
            body=json.dumps(self.PAYLOAD),
            headers={'Content-Type': 'application/json;charset=UTF-8'},
        )

    def parse(self, response, **kwargs):
        item = PricesScrapeItem()
        data = json.loads(response.body)
        loader = HellogetsafeLoader(item=item, response=response)

        loader.add_value('price', self._parse_price(data))
        loader.add_value('currency', 'EUR')

        loader.load_item()
        yield item

    @staticmethod
    def _parse_price(data):
        expr = 'product_configurations[].price.gross_premium'
        prices = jmespath.search(expr, data)
        if prices:
            return sum((float(price) for price in prices if price))

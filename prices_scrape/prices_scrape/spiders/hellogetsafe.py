import json
import jmespath
from datetime import date

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

    DEFAULT_ZIP_CODE = '01067'
    DEFAULT_FAMILY_COVERAGE = False
    DEFAULT_DRONE_COVERAGE = False
    PAYLOAD = {}

    def __init__(
            self,
            zip_code=DEFAULT_ZIP_CODE,
            family_coverage=DEFAULT_FAMILY_COVERAGE,
            drone_coverage=DEFAULT_DRONE_COVERAGE,
            *a,
            **kw
    ):
        super().__init__(*a, **kw)
        true_values = ('1', 1, True, 'true', 'True')

        self.zip_code = zip_code

        self.family_coverage = family_coverage
        self.family_coverage = self.family_coverage in true_values

        self.drone_coverage = drone_coverage
        self.drone_coverage = self.drone_coverage in true_values

        self.PAYLOAD = {
            "product_configurations": [
                {
                    "product_key": "liability_premium_basic_neodigital_de",
                    "configuration_data": {
                        "deductible_amount": 0,
                        "family_coverage": self.family_coverage,
                        "zip_code": self.zip_code,
                        "number_of_claims_in_last_5y": 0
                    },
                    "effective_on": str(date.today())
                },
                {
                    "product_key": "liability_premium_drones_neodigital_de",
                    "configuration_data": {
                        "deductible_amount": 0,
                        "family_coverage": self.family_coverage,
                        "zip_code": self.zip_code,
                        "number_of_claims_in_last_5y": 0
                    },
                    "effective_on": str(date.today())
                }
            ]
        }
        if not self.drone_coverage:
            del self.PAYLOAD.get('product_configurations')[1]

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

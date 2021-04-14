import jmespath
import json

import scrapy
from scrapy import Request


class HellogetsafeSpider(scrapy.Spider):
    name = 'hellogetsafe'
    allowed_domains = ['hellogetsafe.com',
                       'www.hellogetsafe.com',
                       'https://insurance-service.api.getsafe.eu']

    DEFAULT_ZIP_CODE = '01067'
    DEFAULT_FAMILY_COVERAGE = False

    def __init__(self, *a, **kw):
        super(HellogetsafeSpider, self).__init__(*a, **kw)
        self.zip_code = kw.get('zip_code', self.DEFAULT_ZIP_CODE)
        self.family_coverage = kw.get('family_coverage', self.DEFAULT_FAMILY_COVERAGE)
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
                    "effective_on": "2021-04-14"
                }
            ]
        }

    def start_requests(self):
        yield Request(
            url='https://insurance-service.api.getsafe.eu/api/v2/markets/de/prices',
            method='POST',
            body=json.dumps(self.PAYLOAD),
            headers={'Content-Type': 'application/json;charset=UTF-8'},
        )

    def parse(self, response, **kwargs):
        pass

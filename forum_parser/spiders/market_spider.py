import scrapy
from scrapy import Selector
from forum_parser.spiders.utils import clean_article_text
from forum_parser.spiders.utils import get_custom_settings


class InternetMarketSpider(scrapy.Spider):
    name = "freedelivery_site"
    product_count = 20
    filename = "internet_market_result.xml"
    custom_settings = get_custom_settings(
        filename, "scrapy.exporters.XmlItemExporter"
    )

    def start_requests(self):
        base_url = "https://freedelivery.com.ua"
        return [scrapy.Request(url=base_url, callback=self.parse)]

    def parse_products(self, response):
        product_block = Selector(response=response).xpath(
            "//div[contains(@class, 'product-layout')]/div"
        )

        for product in product_block:
            if self.product_count == 0:
                return
            product_image = product.xpath(
                ".//div[@class='image']/a/img/@src"
            ).get()
            product_description_block = product.xpath(".//div[2]/div/div")
            product_description = clean_article_text(
                product_description_block.xpath(
                    ".//p[@class='description']/text()"
                ).get()
            )
            product_price = clean_article_text(
                product_description_block.xpath(
                    ".//div/p[@class='price']/text()"
                ).get()
            )
            self.product_count -= 1

            yield {
                "image": product_image,
                "description": product_description.strip(),
                "price": product_price.strip(),
            }

    def parse(self, response):
        latest_products_url = (
            Selector(response=response)
            .xpath("//div[@class='panel-heading']/a/@href")
            .extract_first()
        )
        request = response.follow(
            latest_products_url, callback=self.parse_products
        )
        yield request

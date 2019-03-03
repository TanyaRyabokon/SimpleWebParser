import re
import scrapy
from scrapy import Selector
from forum_parser.spiders.utils import clean_article_text
from forum_parser.spiders.utils import get_custom_settings


class DorogaSiteSpider(scrapy.Spider):
    name = "doroga_site"
    page_count = 20
    escape_text_fragments = re.compile("^[.: ]$")
    filename = "forum_parse_result.xml"
    custom_settings = get_custom_settings(
        filename, "forum_parser.exporters.ArticlesXmlItemExporter"
    )

    def start_requests(self):
        base_url = "http://www.doroga.ua/"
        return [scrapy.Request(url=base_url, callback=self.parse)]

    def parse_article(self, response):
        article_block = Selector(response=response).xpath(
            "//td[@class='main-column center']/div/div/div[2]"
        )

        article_header_block = article_block.xpath(
            "./span[1]/table[1]/tr/td/div[1]/span/text()"
        ).extract_first()

        article_images = (
            Selector(response=response)
            .xpath(
                "//descendant-or-self::*[img]/img/@src".format(
                    article_header_block
                )
            )
            .extract()
        )

        article_text = list(
            map(
                clean_article_text,
                article_block.xpath(
                    "//descendant-or-self::*[p]/p/text()"
                ).extract(),
            )
        )

        article_next_urls = article_block.xpath(
            "//div[@class='SectionHeader']/"
            "following-sibling::div[1]/div/a/@href"
        ).extract()

        yield {
            "url": response.url,
            "image": article_images,
            "text": [
                text
                for text in article_text
                if not self.escape_text_fragments.match(text)
            ],
        }

        for next_url in article_next_urls:
            if self.page_count == 0:
                return None
            self.page_count -= 1
            yield response.follow(next_url, callback=self.parse_article)

    def parse(self, response):
        first_article_url = (
            Selector(response=response)
            .xpath(
                "//td[@class='main-column center']/div[3]/table[1]"
                "/tr/td[2]/div[1]/a/@href"
            )
            .extract_first()
        )
        request = scrapy.Request(
            first_article_url, callback=self.parse_article
        )
        yield request

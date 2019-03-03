from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from forum_analyzer.calculate_elements import find_min_images_count
from data_converter.xml_to_html import xml_data_to_html
from forum_parser.spiders.doroga_spider import DorogaSiteSpider
from forum_parser.spiders.market_spider import InternetMarketSpider


# wrapper to run multiple spiders in one process
def run_spider(spider):
    def run(q):
        print("Crawl {}".format(spider.name))
        try:
            runner = CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    queue = Queue()
    p = Process(target=run, args=(queue,))
    p.start()
    result = queue.get()
    p.join()

    if result is not None:
        raise result


def main():
    print("Task 1: Parse forum\n")
    run_spider(DorogaSiteSpider)
    print(
        "minimum number of pictures per page is {}".format(
            find_min_images_count(DorogaSiteSpider.filename)
        )
    )

    print("Task 2: Parse internet market\n")

    run_spider(InternetMarketSpider)
    xml_data_to_html(InternetMarketSpider.filename, "products.html")


if __name__ == "__main__":
    main()

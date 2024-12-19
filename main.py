from json import dump
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from spiders.tender import LPSESpiderTender


# Save data after spider finishes
def save_tender_data(spider):
    with open("output/data_tender.json", "w", encoding="utf-8") as file:
        dump(spider.data, file, ensure_ascii=False, indent=4)
    print("Data saved to output/data_tender.json")


# Run the Spider
process = CrawlerProcess()

# Run Tender Spider
dispatcher.connect(save_tender_data, signal=signals.spider_closed, weak=False)
process.crawl(LPSESpiderTender)

process.start()

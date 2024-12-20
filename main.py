from json import dump
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from spiders.tender import LPSESpiderTender
from downloader.tender import download_tender_data
from preprocessing.tender import clean_tender_data
from analyzer.tender import analyze_tender


def run_downloader():
    download_tender_data()


def run_spiders():
    # Save data after spider finishes
    def save_tender_data(spider):
        with open("data/spiders/data_tender.json", "w", encoding="utf-8") as file:
            dump(spider.data, file, ensure_ascii=False, indent=4)
        print("Data saved to data/spiders/data_tender.json")

    # Run the Spider
    process = CrawlerProcess()

    # Run Tender Spider
    dispatcher.connect(save_tender_data, signal=signals.spider_closed, weak=False)
    process.crawl(LPSESpiderTender)

    process.start()


def run_preprocessing():
    clean_tender_data()


# Run downloader first
# run_downloader()

# Run the spider
# run_spiders()

# Run preprocessing
# clean_tender_data()

# Run analyzer
analyze_tender(
    jenis_tender=None,
    tahapan="Tender Sudah Selesai",
    mulai_tahun=2020,
    selesai_tahun=2024,
)

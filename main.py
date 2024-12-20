from json import dump
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from spiders.tender import LPSESpiderTender
from downloader.tender import download_tender_data
from preprocessing.tender import clean_tender_data
from analyzer.tender import TenderAnalyzer


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
tender_analyzer = TenderAnalyzer()
tender_analyzer.filter_and_group_tender_data(
    tender_type=None,
    phase="Tender Sudah Selesai",
    start_year=2020,
    end_year=2024,
)
tender_analyzer.visualize_tender_data(visualize_tender_type="Jumlah Tender", top=20)

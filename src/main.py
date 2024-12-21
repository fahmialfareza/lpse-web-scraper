from downloader.main import run_downloader
from spiders.main import run_spiders
from preprocessing.main import run_preprocessing
from analyzer.main import run_analyzer


# Run downloader first
# run_downloader()

# Run the spider
# run_spiders()

# Run preprocessing
# run_preprocessing()

# Run analyzer
run_analyzer(visualize_tender_type="Total Harga Penawaran")

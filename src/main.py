from downloader.main import run_downloader
from spiders.main import run_spiders
from preprocessing.main import run_preprocessing
from analyzer.main import run_analyzer
from db.main import save_to_db


# Run downloader first
# run_downloader()

# Run the spider
# run_spiders()

# Save to db
# save_to_db()

# Run analyzer
run_analyzer()

from downloader.tender import download_tender_data


def run_downloader():
    """Run the tender data downloader.

    This function is the entry point for the tender data downloader. It calls the
    download_tender_data function to download the tender data.

    Returns:
        None
    Raises:
        None
    """

    download_tender_data()

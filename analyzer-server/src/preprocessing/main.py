from preprocessing.tender import clean_tender_data


def run_preprocessing():
    """Run the preprocessing pipeline.

    This function runs the preprocessing pipeline, which includes cleaning and preprocessing the tender data.

    Returns:
        None
    """

    tenders_clean = clean_tender_data()

    data = dict()
    data["Tender"] = tenders_clean
    return data

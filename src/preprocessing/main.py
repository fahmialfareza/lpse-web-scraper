from preprocessing.tender import clean_tender_data


def run_preprocessing():
    """Run the preprocessing pipeline.

    This function runs the preprocessing pipeline, which includes cleaning and preprocessing the tender data.

    Returns:
        None
    """

    clean_tender_data()

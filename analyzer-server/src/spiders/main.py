from spiders.tender import run_tender_spiders


def run_spiders():
    """Run spiders

    This function runs the spiders for the tender data.
    The spiders are defined in the spiders directory.
    The spiders are run in the following order:
    - tender
    """

    return run_tender_spiders()

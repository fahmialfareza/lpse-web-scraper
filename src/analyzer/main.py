from analyzer.tender import run_tender_analyzer


def run_analyzer(
    data_type="tender",
    tender_type=None,
    phase=None,
    start_year=None,
    end_year=None,
    visualize_tender_type="Jumlah Tender",
    top=10,
):
    """Run analyzer based on data type

    Args:
        data_type (str): Data type to be analyzed
        tender_type (str): Tender type to be analyzed
        phase (str): Phase to be analyzed
        start_year (int): Start year to be analyzed
        end_year (int): End year
        visualize_tender_type (str): Tender type to be visualized
        top (int): Top number of data to be visualized
    Returns:
        None
    Raises:
        ValueError: If data type is not valid
    Examples:
        run_analyzer(data_type="tender", tender_type="Jasa", phase="Pengadaan", start_year=2020, end_year=2022, visualize_tender_type="Jumlah Tender", top=10)
    """
    match data_type:
        case "tender":
            run_tender_analyzer(
                end_year=end_year,
                phase=phase,
                start_year=start_year,
                tender_type=tender_type,
                top=top,
                visualize_tender_type=visualize_tender_type,
            )
        case _:
            print("Invalid data type")

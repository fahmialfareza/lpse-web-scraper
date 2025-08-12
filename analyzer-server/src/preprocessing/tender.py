from json import load, dump
from utils.converter import convert_currency_to_int, convert_date_string_to_date
from os.path import dirname, join, abspath
from db.main import get_tender_data


def clean_tender_data():
    """Clean the tender data by removing unnecessary keys and converting currency values to integers.

    Returns:
        list: A list of dictionaries containing the cleaned tender data.
    Raises:
        ValueError: If the tender data is not in the expected format.
    """

    # Get tender data
    tenders = get_tender_data()
    data = list()
    for tender in tenders:
        if tender.get("HPS"):
            tender["HPS"] = convert_currency_to_int(tender["HPS"])
        if tender.get("Nilai Pagu Paket"):
            tender["Nilai Pagu Paket"] = convert_currency_to_int(
                tender["Nilai Pagu Paket"]
            )
        if tender.get("Nilai HPS Paket"):
            tender["Nilai HPS Paket"] = convert_currency_to_int(
                tender["Nilai HPS Paket"]
            )
        if tender.get("Pagu"):
            tender["Pagu"] = convert_currency_to_int(tender["Pagu"])
        if tender.get("Harga Penawaran"):
            tender["Harga Penawaran"] = convert_currency_to_int(
                tender["Harga Penawaran"]
            )
        if tender.get("Harga Terkoreksi"):
            tender["Harga Terkoreksi"] = convert_currency_to_int(
                tender["Harga Terkoreksi"]
            )
        if tender.get("Tanggal Pembuatan"):
            tender["Tanggal Pembuatan"] = convert_date_string_to_date(
                tender["Tanggal Pembuatan"]
            )

        data.append(tender)

    # Get the path to the 'data' directory
    return data

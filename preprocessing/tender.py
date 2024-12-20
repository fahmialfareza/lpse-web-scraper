from json import load, dump
from utils.converter import convert_currency_to_int, convert_date_string_to_date


def clean_tender_data():
    with open("data/spiders/data_tender_all.json", "r") as file:
        tenders = load(file)
    data = list()
    for tender in tenders.values():
        if tender.get("Pengumuman"):
            tender.update(tender["Pengumuman"])
            del tender["Pengumuman"]
        if tender.get("Pemenang"):
            tender.update(tender["Pemenang"])
            del tender["Pemenang"]
        if tender.get("Pemenang Berkontrak"):
            tender.update(tender["Pemenang Berkontrak"])
            del tender["Pemenang Berkontrak"]
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

    with open("data/preprocessing/data_tender.json", "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)
        print("Data saved to data/preprocessing/data_tender.json")

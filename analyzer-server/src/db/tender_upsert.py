from os.path import dirname, join, abspath
from db.connection import engine
from json import load
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from db.tender_model import (
    Tender,
    TenderPengumuman,
    TenderPeserta,
    TenderPemenang,
    TenderPemenangBerkontrak,
)


def save_to_tender_db():
    # Get the path to the 'data' directory
    base_dir = dirname(dirname(abspath(__file__)))
    data_dir = join(base_dir, "..", "data", "spiders")
    file_path = join(data_dir, "data_tender.json")

    with open(file_path, "r") as file:
        tenders = load(file)

    # Prepare data for upsert
    tenders_db = list()
    tender_pengumuman_db = list()
    tender_peserta_db = list()
    tender_pemenang_db = list()
    tender_pemenang_berkontrak_db = list()

    for tender in tenders.values():
        # Prepare data for the tender table
        tenders_db.append(
            {
                "kode": tender.get("Kode"),
                "Nama Paket": tender.get("Nama Paket"),
                "K/L/PD/Instansi Lainnya": tender.get("K/L/PD/Instansi Lainnya"),
                "tahapan": tender.get("Tahapan"),
                "hps": tender.get("HPS"),
            }
        )
        # Prepare data for the tender_pengumuman table if "Pengumuman" exists
        if tender.get("Pengumuman"):
            tender_pengumuman_db.append(
                {
                    "Kode Tender": tender.get("Kode"),
                    "Nama Tender": tender["Pengumuman"].get("Nama Tender"),
                    "Rencana Umum Pengadaan": tender["Pengumuman"].get(
                        "Rencana Umum Pengadaan"
                    ),
                    "Uraian Singkat Pekerjaan": tender["Pengumuman"].get(
                        "Uraian Singkat Pekerjaan"
                    ),
                    "Tanggal Pembuatan": tender["Pengumuman"].get("Tanggal Pembuatan"),
                    "Tahap Tender Saat Ini": tender["Pengumuman"].get(
                        "Tahap Tender Saat Ini"
                    ),
                    "K/L/PD/Instansi Lainnya": tender["Pengumuman"].get(
                        "K/L/PD/Instansi Lainnya"
                    ),
                    "Satuan Kerja": tender["Pengumuman"].get("Satuan Kerja"),
                    "Jenis Pengadaan": tender["Pengumuman"].get("Jenis Pengadaan"),
                    "Metode Pengadaan": tender["Pengumuman"].get("Metode Pengadaan"),
                    "Khusus Orang Asli Papua (OAP)": tender["Pengumuman"].get(
                        "Khusus Orang Asli Papua (OAP)"
                    ),
                    "Tahun Anggaran": tender["Pengumuman"].get("Tahun Anggaran"),
                    "Nilai Pagu Paket": tender["Pengumuman"].get("Nilai Pagu Paket"),
                    "Nilai HPS Paket": tender["Pengumuman"].get("Nilai HPS Paket"),
                    "Jenis Kontrak": tender["Pengumuman"].get("Jenis Kontrak"),
                    "Lokasi Pekerjaan": tender["Pengumuman"].get("Lokasi Pekerjaan"),
                    "Bobot Teknis": tender["Pengumuman"].get("Bobot Teknis"),
                    "Bobot Biaya": tender["Pengumuman"].get("Bobot Biaya"),
                    "Syarat Kualifikasi": tender["Pengumuman"].get(
                        "Syarat Kualifikasi"
                    ),
                    "Peserta Tender": tender["Pengumuman"].get("Peserta Tender"),
                }
            )
            # Prepare data for the TenderPeserta table
        if tender.get("Peserta"):
            for peserta in tender["Peserta"]:
                tender_peserta_db.append(
                    {
                        "Kode Tender": tender.get("Kode"),
                        "No": peserta.get("No"),
                        "Nama Peserta": peserta.get("Nama Peserta"),
                        "npwp": peserta.get("NPWP"),
                        "Harga Penawaran": peserta.get("Harga Penawaran"),
                        "Harga Terkoreksi": peserta.get("Harga Terkoreksi"),
                    }
                )
        # Prepare data for the TenderPemenang table
        if tender.get("Pemenang"):
            tender_pemenang_db.append(
                {
                    "Kode Tender": tender.get("Kode"),
                    "Nama Tender": tender["Pemenang"].get("Nama Tender"),
                    "Jenis Pengadaan": tender["Pemenang"].get("Jenis Pengadaan"),
                    "K/L/PD/Instansi Lainnya": tender["Pemenang"].get(
                        "K/L/PD/Instansi Lainnya"
                    ),
                    "Satuan Kerja": tender["Pemenang"].get("Satuan Kerja"),
                    "pagu": tender["Pemenang"].get("Pagu"),
                    "hps": tender["Pemenang"].get("HPS"),
                    "Nama Pemenang": tender["Pemenang"].get("Nama Pemenang"),
                    "alamat": tender["Pemenang"].get("Alamat"),
                    "npwp": tender["Pemenang"].get("NPWP"),
                    "Harga Penawaran": tender["Pemenang"].get("Harga Penawaran"),
                    "Harga Terkoreksi": tender["Pemenang"].get("Harga Terkoreksi"),
                    "Harga Negosiasi": tender["Pemenang"].get("Harga Negosiasi"),
                }
            )
        # Prepare data for the TenderPemenangBerkontrak table
        if tender.get("Pemenang Berkontrak"):
            tender_pemenang_berkontrak_db.append(
                {
                    "Kode Tender": tender.get("Kode"),
                    "Nama Tender": tender["Pemenang Berkontrak"].get("Nama Tender"),
                    "Jenis Pengadaan": tender["Pemenang Berkontrak"].get(
                        "Jenis Pengadaan"
                    ),
                    "K/L/PD/Instansi Lainnya": tender["Pemenang Berkontrak"].get(
                        "K/L/PD/Instansi Lainnya"
                    ),
                    "Satuan Kerja": tender["Pemenang Berkontrak"].get("Satuan Kerja"),
                    "pagu": tender["Pemenang Berkontrak"].get("Pagu"),
                    "hps": tender["Pemenang Berkontrak"].get("HPS"),
                    "Nama Pemenang": tender["Pemenang Berkontrak"].get("Nama Pemenang"),
                    "alamat": tender["Pemenang Berkontrak"].get("Alamat"),
                    "npwp": tender["Pemenang Berkontrak"].get("NPWP"),
                    "Harga Kontrak": tender["Pemenang Berkontrak"].get("Harga Kontrak"),
                    "Nilai PDN": tender["Pemenang Berkontrak"].get("Nilai PDN"),
                    "Nilai UMK": tender["Pemenang Berkontrak"].get("Nilai UMK"),
                }
            )

    def insert_tender_data():
        try:
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Upsert for the tender table
            tender_stmt = insert(Tender).values(tenders_db)
            tender_upsert_stmt = tender_stmt.on_conflict_do_update(
                index_elements=["kode"],
                set_={
                    "Nama Paket": tender_stmt.excluded.get("Nama Paket"),
                    "K/L/PD/Instansi Lainnya": tender_stmt.excluded.get(
                        "K/L/PD/Instansi Lainnya"
                    ),
                    "tahapan": tender_stmt.excluded.get("tahapan"),
                    "hps": tender_stmt.excluded.get("hps"),
                },
            )
            session.execute(tender_upsert_stmt)

            # Commit the transaction
            session.commit()
            print("Upsert operation successful.")
        except Exception as e:
            # Rollback in case of error
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            # Close the session
            session.close()

    def insert_tender_pengumuman_data():
        try:
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Upsert for the tender_pengumuman table
            if tender_pengumuman_db:
                pengumuman_stmt = insert(TenderPengumuman).values(tender_pengumuman_db)
                pengumuman_upsert_stmt = pengumuman_stmt.on_conflict_do_update(
                    index_elements=["Kode Tender"],
                    set_={
                        "Nama Tender": pengumuman_stmt.excluded.get("Nama Tender"),
                        "Rencana Umum Pengadaan": pengumuman_stmt.excluded.get(
                            "Rencana Umum Pengadaan"
                        ),
                        "Uraian Singkat Pekerjaan": pengumuman_stmt.excluded.get(
                            "Uraian Singkat Pekerjaan"
                        ),
                        "Tanggal Pembuatan": pengumuman_stmt.excluded.get(
                            "Tanggal Pembuatan"
                        ),
                        "Tahap Tender Saat Ini": pengumuman_stmt.excluded.get(
                            "Tahap Tender Saat Ini"
                        ),
                        "K/L/PD/Instansi Lainnya": pengumuman_stmt.excluded.get(
                            "K/L/PD/Instansi Lainnya"
                        ),
                        "Satuan Kerja": pengumuman_stmt.excluded.get("Satuan Kerja"),
                        "Jenis Pengadaan": pengumuman_stmt.excluded.get(
                            "Jenis Pengadaan"
                        ),
                        "Metode Pengadaan": pengumuman_stmt.excluded.get(
                            "Metode Pengadaan"
                        ),
                        "Khusus Orang Asli Papua (OAP)": pengumuman_stmt.excluded.get(
                            "Khusus Orang Asli Papua (OAP)"
                        ),
                        "Tahun Anggaran": pengumuman_stmt.excluded.get(
                            "Tahun Anggaran"
                        ),
                        "Nilai Pagu Paket": pengumuman_stmt.excluded.get(
                            "Nilai Pagu Paket"
                        ),
                        "Nilai HPS Paket": pengumuman_stmt.excluded.get(
                            "Nilai HPS Paket"
                        ),
                        "Jenis Kontrak": pengumuman_stmt.excluded.get("Jenis Kontrak"),
                        "Lokasi Pekerjaan": pengumuman_stmt.excluded.get(
                            "Lokasi Pekerjaan"
                        ),
                        "Bobot Teknis": pengumuman_stmt.excluded.get("Bobot Teknis"),
                        "Bobot Biaya": pengumuman_stmt.excluded.get("Bobot Biaya"),
                        "Syarat Kualifikasi": pengumuman_stmt.excluded.get(
                            "Syarat Kualifikasi"
                        ),
                        "Peserta Tender": pengumuman_stmt.excluded.get(
                            "Peserta Tender"
                        ),
                    },
                )
                session.execute(pengumuman_upsert_stmt)

            # Commit the transaction
            session.commit()
            print("Upsert operation successful.")
        except Exception as e:
            # Rollback in case of error
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            # Close the session
            session.close()

    def insert_tender_peserta_data():
        try:
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            if tender_peserta_db:
                peserta_stmt = insert(TenderPeserta).values(tender_peserta_db)
                peserta_upsert_stmt = peserta_stmt.on_conflict_do_update(
                    index_elements=["Kode Tender", "No"],
                    set_={
                        "Nama Peserta": peserta_stmt.excluded.get("Nama Peserta"),
                        "Harga Penawaran": peserta_stmt.excluded.get("Harga Penawaran"),
                        "npwp": peserta_stmt.excluded.get("npwp"),
                        "Harga Terkoreksi": peserta_stmt.excluded.get(
                            "Harga Terkoreksi"
                        ),
                    },
                )
                session.execute(peserta_upsert_stmt)

            # Commit the transaction
            session.commit()
            print("Upsert operation successful.")
        except Exception as e:
            # Rollback in case of error
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            # Close the session
            session.close()

    def insert_tender_pemenang_data():
        try:
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            if tender_pemenang_db:
                pemenang_stmt = insert(TenderPemenang).values(tender_pemenang_db)
                pemenang_upsert_stmt = pemenang_stmt.on_conflict_do_update(
                    index_elements=["Kode Tender"],
                    set_={
                        "Kode Tender": pemenang_stmt.excluded.get("Kode"),
                        "Nama Tender": pemenang_stmt.excluded.get("Nama Tender"),
                        "Jenis Pengadaan": pemenang_stmt.excluded.get(
                            "Jenis Pengadaan"
                        ),
                        "K/L/PD/Instansi Lainnya": pemenang_stmt.excluded.get(
                            "K/L/PD/Instansi Lainnya"
                        ),
                        "Satuan Kerja": pemenang_stmt.excluded.get("Satuan Kerja"),
                        "pagu": pemenang_stmt.excluded.get("pagu"),
                        "hps": pemenang_stmt.excluded.get("hps"),
                        "Nama Pemenang": pemenang_stmt.excluded.get("Nama Pemenang"),
                        "alamat": pemenang_stmt.excluded.get("alamat"),
                        "npwp": pemenang_stmt.excluded.get("npwp"),
                        "Harga Penawaran": pemenang_stmt.excluded.get(
                            "Harga Penawaran"
                        ),
                        "Harga Terkoreksi": pemenang_stmt.excluded.get(
                            "Harga Terkoreksi"
                        ),
                        "Harga Negosiasi": pemenang_stmt.excluded.get(
                            "Harga Negosiasi"
                        ),
                    },
                )
                session.execute(pemenang_upsert_stmt)

            # Commit the transaction
            session.commit()
            print("Upsert operation successful.")
        except Exception as e:
            # Rollback in case of error
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            # Close the session
            session.close()

    def insert_tender_pemenang_berkontrak_data():
        try:
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            if tender_pemenang_berkontrak_db:
                pemenang_berkontrak_stmt = insert(TenderPemenangBerkontrak).values(
                    tender_pemenang_berkontrak_db
                )
                pemenang_berkontrak_stmt = pemenang_berkontrak_stmt.on_conflict_do_update(
                    index_elements=["Kode Tender"],
                    set_={
                        "Kode Tender": pemenang_berkontrak_stmt.excluded.get("Kode"),
                        "Nama Tender": pemenang_berkontrak_stmt.excluded.get(
                            "Nama Tender"
                        ),
                        "Jenis Pengadaan": pemenang_berkontrak_stmt.excluded.get(
                            "Jenis Pengadaan"
                        ),
                        "K/L/PD/Instansi Lainnya": pemenang_berkontrak_stmt.excluded.get(
                            "K/L/PD/Instansi Lainnya"
                        ),
                        "Satuan Kerja": pemenang_berkontrak_stmt.excluded.get(
                            "Satuan Kerja"
                        ),
                        "pagu": pemenang_berkontrak_stmt.excluded.get("pagu"),
                        "hps": pemenang_berkontrak_stmt.excluded.get("hps"),
                        "Nama Pemenang": pemenang_berkontrak_stmt.excluded.get(
                            "Nama Pemenang"
                        ),
                        "alamat": pemenang_berkontrak_stmt.excluded.get("alamat"),
                        "npwp": pemenang_berkontrak_stmt.excluded.get("npwp"),
                        "Harga Kontrak": pemenang_berkontrak_stmt.excluded.get(
                            "Harga Kontrak"
                        ),
                        "Nilai PDN": pemenang_berkontrak_stmt.excluded.get("Nilai PDN"),
                        "Nilai UMK": pemenang_berkontrak_stmt.excluded.get("Nilai UMK"),
                    },
                )
                session.execute(pemenang_berkontrak_stmt)

            # Commit the transaction
            session.commit()
            print("Upsert operation successful.")
        except Exception as e:
            # Rollback in case of error
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            # Close the session
            session.close()

    # Insert to db
    insert_tender_data()
    insert_tender_pengumuman_data()
    insert_tender_peserta_data()
    insert_tender_pemenang_data()
    insert_tender_pemenang_berkontrak_data()

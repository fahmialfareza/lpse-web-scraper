from sqlalchemy import text
from db.connection import engine


def fetch_left_join_tender_results():
    # Define the raw SQL query
    query = text(
        """
        SELECT 
            t.kode AS "Kode",
            t."Nama Paket" AS "Nama Paket",
            t."K/L/PD/Instansi Lainnya" AS "K/L/PD/Instansi Lainnya",
            t.tahapan AS "Tahapan",
            t.hps AS "HPS",
            tp."Nama Tender" AS "Nama Tender",
            tp."Rencana Umum Pengadaan" AS "Rencana Umum Pengadaan",
            tp."Tanggal Pembuatan" AS "Tanggal Pembuatan",
            tp."Tahap Tender Saat Ini" AS "Tahap Tender Saat Ini",
            tp."Satuan Kerja" AS "Satuan Kerja",
            tp."Jenis Pengadaan" AS "Jenis Pengadaan",
            tp."Metode Pengadaan" AS "Metode Pengadaan",
            tp."Khusus Orang Asli Papua (OAP)" AS "Khusus Orang Asli Papua (OAP)",
            tp."Tahun Anggaran" AS "Tahun Anggaran",
            tp."Nilai Pagu Paket" AS "Nilai Pagu Paket",
            tp."Nilai HPS Paket" AS "Nilai HPS Paket",
            tp."Jenis Kontrak" AS "Jenis Kontrak",
            tp."Lokasi Pekerjaan" AS "Lokasi Pekerjaan",
            tp."Syarat Kualifikasi" AS "Syarat Kualifikasi",
            tpb."Nama Pemenang" AS "Nama Pemenang",
            tpb.alamat AS "Alamat",
            tpb.npwp AS "NPWP",
            tpb.pagu AS "Pagu",
            tpem."Harga Penawaran" AS "Harga Penawaran",
            tpem."Harga Terkoreksi" AS "Harga Terkoreksi",
            tpem."Harga Negosiasi" AS "Harga Negosiasi",
            tpb."Harga Kontrak" AS "Harga Kontrak",
            tpb."Nilai PDN" AS "Nilai PDN",
            tpb."Nilai UMK" AS "Nilai UMK"
        FROM public.tender t
        LEFT JOIN public.tender_pengumuman tp ON t.kode = tp."Kode Tender"
        LEFT JOIN public.tender_pemenang tpem ON t.kode = tpem."Kode Tender"
        LEFT JOIN public.tender_pemenang_berkontrak tpb ON t.kode = tpb."Kode Tender"
    """
    )

    # Execute the query
    with engine.connect() as conn:
        results = conn.execute(query)

    # Process results into a list of dictionaries
    rows = [dict(row) for row in results.mappings()]

    return rows

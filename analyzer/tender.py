import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from utils.converter import rupiah_format


def analyze_tender(
    tahapan=None, mulai_tahun=None, selesai_tahun=None, jenis_tender=None
):
    """Analyze tender

    Args:
        tahapan (str): Tahapan tender
                - "Tender Gagal"
                - "Tender Sudah Selesai"
                - "Seleksi Gagal"
                - "Masa Sanggah"
        tahun (int): Tahun tender
        jenis_tender (str): Jenis tender
                - "Pengadaan Barang"
                - "Pekerjaan Konstruksi"
                - "Jasa Konsultansi Badan Usaha Non Konstruksi"
                - "Jasa Konsultansi Badan Usaha Konstruksi"
                - "Jasa Konsultansi Perorangan Non Konstruksi"
                - "Jasa Konsultansi Perorangan Konstruksi"
                - "Jasa Lainnya"
                - "Pekerjaan Konstruksi Terintegrasi"
    """
    df = pd.read_json(
        "data/preprocessing/data_tender.json", convert_dates=["Tanggal Pembuatan"]
    )

    # Convert numeric columns to proper numeric types
    numeric_columns = [
        "Harga Penawaran",
        "Harga Terkoreksi",
        "Pagu",
        "Nilai HPS Paket",
        "Nilai Pagu Paket",
        "HPS",
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )  # Convert to numeric, replace non-numeric with NaN

    # Apply filters only if arguments are provided
    if tahapan:
        df = df[df["Tahapan"] == tahapan]
    if jenis_tender:
        df = df[df["Jenis Pengadaan"] == jenis_tender]
    if mulai_tahun and selesai_tahun:
        df = df[
            (df["Tanggal Pembuatan"].dt.year >= mulai_tahun)
            & (df["Tanggal Pembuatan"].dt.year <= selesai_tahun)
        ]

    # Group by 'Nama Pemenang'
    grouped_data = (
        df.groupby("Nama Pemenang")
        .agg(
            {
                "Nama Pemenang": "size",  # Count occurrences of 'Nama Pemenang'
                "Harga Penawaran": "sum",
                "Harga Terkoreksi": "sum",
                "Pagu": "sum",
                "Nilai HPS Paket": "sum",
                "Nilai Pagu Paket": "sum",
                "HPS": "sum",
            }
        )
        .rename(columns={"Nama Pemenang": "Count"})
    )

    # Reset index for better readability
    grouped_data = grouped_data.reset_index()

    # Get top 10 by Count
    top_10_count = grouped_data.nlargest(10, "Count")

    # Plotting the Top 10 Count of Nama Pemenang
    plt.figure(figsize=(10, 6))
    plt.bar(top_10_count["Nama Pemenang"], top_10_count["Count"])
    plt.xlabel("Nama Pemenang")
    plt.ylabel("Jumlah Tender")
    plt.title(
        f"Top 10 Jumlah Tender Dengan Jenis Pengadaan {jenis_tender or 'Semua'} Berdasarkan Pemenang Tender Tahun {mulai_tahun or 'Awal'} - {selesai_tahun or 'Akhir'}"
    )
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    # Get top 10 by Harga Penawaran
    top_10_harga_penawaran = grouped_data.nlargest(10, "Harga Penawaran")

    # Plotting the Top 10 Harga Penawaran
    formatter = FuncFormatter(rupiah_format)
    plt.figure(figsize=(10, 6))
    plt.bar(
        top_10_harga_penawaran["Nama Pemenang"],
        top_10_harga_penawaran["Harga Penawaran"],
    )
    plt.xlabel("Nama Pemenang")
    plt.ylabel("Total Harga Penawaran")
    plt.title(
        f"Top 10 Total Harga Penawaran Dengan Jenis Pengadaan {jenis_tender or 'Semua'} Berdasarkan Pemenang Tender Tahun {mulai_tahun or 'Awal'} - {selesai_tahun or 'Akhir'}"
    )
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.show()

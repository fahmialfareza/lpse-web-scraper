import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from utils.converter import rupiah_format


def analyze_tender(tahapan, tahun, jenis_tender):
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

    # Filter rows where 'Tahapan' is 'Tender Sudah Selesai',
    # 'Jenis Pengadaan' is 'Jasa Lainnya', and 'Tanggal Pembuatan' is in 2024
    filtered_data = df[
        (df["Tahapan"] == tahapan)
        & (df["Jenis Pengadaan"] == jenis_tender)
        & (df["Tanggal Pembuatan"].dt.year == tahun)
    ]

    # Group by 'Nama Pemenang'
    grouped_data = (
        filtered_data.groupby("Nama Pemenang")
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

    # Display the results
    # Plotting the Count of Nama Pemenang
    plt.figure(figsize=(10, 6))
    plt.bar(grouped_data["Nama Pemenang"], grouped_data["Count"])
    plt.xlabel("Nama Pemenang")
    plt.ylabel("Jumlah Tender")
    plt.title(
        f"Jumlah Tender Dengan Jenis Pengadaan {jenis_tender} Berdasarkan Pemenang Tender Tahun {tahun}"
    )
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    # Plotting the Sum of Harga Penawaran
    formatter = FuncFormatter(rupiah_format)
    plt.figure(figsize=(10, 6))
    plt.bar(grouped_data["Nama Pemenang"], grouped_data["Harga Penawaran"])
    plt.xlabel("Nama Pemenang")
    plt.ylabel("Total Harga Penawaran")
    plt.title(
        f"Total Harga Penawaran Dengan Jenis Pengadaan {jenis_tender} Berdasarkan Pemenang Tender Tahun {tahun}"
    )
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from utils.converter import rupiah_format


class TenderAnalyzer:
    def __init__(self, tender_data):
        self.grouped_data = pd.DataFrame()
        self.tender_type = None
        self.start_year = None
        self.end_year = None
        self.tender_data = tender_data

    def filter_and_group_tender_data(
        self,
        phase=None,
        start_year=None,
        end_year=None,
        tender_type=None,
        tender_data=None,
    ):
        """Analyze tender

        Args:
            phase (str): Tahapan tender
                    - "Tender Gagal"
                    - "Tender Sudah Selesai"
                    - "Seleksi Gagal"
                    - "Masa Sanggah"
            tahun (int): Tahun tender
            tender_type (str): Jenis tender
                    - "Pengadaan Barang"
                    - "Pekerjaan Konstruksi"
                    - "Jasa Konsultansi Badan Usaha Non Konstruksi"
                    - "Jasa Konsultansi Badan Usaha Konstruksi"
                    - "Jasa Konsultansi Perorangan Non Konstruksi"
                    - "Jasa Konsultansi Perorangan Konstruksi"
                    - "Jasa Lainnya"
                    - "Pekerjaan Konstruksi Terintegrasi"
        """
        self.tender_type = tender_type
        self.start_year = start_year
        self.end_year = end_year

        df = pd.DataFrame(self.tender_data)
        # Convert the 'Date' column to datetime
        df["Tanggal Pembuatan"] = pd.to_datetime(df["Tanggal Pembuatan"])

        if self.start_year == None or self.end_year == None:
            self.start_year = int(df["Tanggal Pembuatan"].dt.year.min())
            self.end_year = int(df["Tanggal Pembuatan"].dt.year.max())

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
        if phase:
            df = df[df["Tahapan"] == phase]
        if tender_type:
            df = df[df["Jenis Pengadaan"] == tender_type]
        if start_year and end_year:
            df = df[
                (df["Tanggal Pembuatan"].dt.year >= start_year)
                & (df["Tanggal Pembuatan"].dt.year <= end_year)
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
        self.grouped_data = grouped_data.reset_index()

    def visualize_tender_data(self, visualize_tender_type="Jumlah Tender", top=10):
        """Visualize tender data

        Args:
            visualize_tender_type (str): Type of visualization to be performed
                - "Jumlah Tender" (default)
                - "Total Harga Penawaran"
            top (int): Number of top results to be displayed
        """

        match visualize_tender_type:
            case "Jumlah Tender":
                # Get top 10 by Count
                top_count = self.grouped_data.nlargest(top, "Count")

                # Plotting the Top 10 Count of Nama Pemenang
                plt.figure(figsize=(10, 6))
                plt.bar(top_count["Nama Pemenang"], top_count["Count"])
                plt.xlabel("Nama Pemenang")
                plt.ylabel("Jumlah Tender")
                plt.title(
                    f"Top {top} Jumlah Tender Dengan Jenis Pengadaan {self.tender_type or 'Semua'} Berdasarkan Pemenang Tender Tahun {self.start_year or 'Awal'} - {self.end_year or 'Akhir'}"
                )
                plt.xticks(rotation=45, ha="right")
                plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
                plt.tight_layout()
                plt.show()

            case "Total Harga Penawaran":
                # Get top 10 by Harga Penawaran
                top_harga_penawaran = self.grouped_data.nlargest(top, "Harga Penawaran")

                # Plotting the Top 10 Harga Penawaran
                formatter = FuncFormatter(rupiah_format)
                plt.figure(figsize=(10, 6))
                plt.bar(
                    top_harga_penawaran["Nama Pemenang"],
                    top_harga_penawaran["Harga Penawaran"],
                )
                plt.xlabel("Nama Pemenang")
                plt.ylabel("Total Harga Penawaran")
                plt.title(
                    f"Top {top} Total Harga Penawaran Dengan Jenis Pengadaan {self.tender_type or 'Semua'} Berdasarkan Pemenang Tender Tahun {self.start_year or 'Awal'} - {self.end_year or 'Akhir'}"
                )
                plt.xticks(rotation=45, ha="right")
                plt.gca().yaxis.set_major_formatter(formatter)
                plt.tight_layout()
                plt.show()

            case _:
                print("Invalid visualization type")


def run_tender_analyzer(
    tender_data=None,
    tender_type=None,
    phase=None,
    start_year=None,
    end_year=None,
    visualize_tender_type="Jumlah Tender",
    top=10,
):
    """Run the tender analyzer with the given parameters.

    Args:
        tender_type (str, optional): The type of tender to analyze. Defaults to None.
        phase (str, optional): The phase of the tender to analyze. Defaults to None.
        start_year (int, optional): The start year of the tender to analyze. Defaults to None.
        end_year (int, optional): The end year of the tender to analyze. Defaults to None.
        visualize_tender_type (str, optional): The type of visualization to perform. Defaults to "Jumlah Tender".
        top (int, optional): The number of top results to display. Defaults to 10.
    Returns:
        None
    Raises:
        ValueError: If the visualize_tender_type is not one of the allowed values.
    Example:
        run_tender_analyzer(tender_type="Pemilihan Pemerintah Daerah", phase="Pengadaan Barang/Jasa", start_year=2020, end_year=2022, visualize_tender_type="Jumlah Tender", top=5)
    """

    tender_analyzer = TenderAnalyzer(tender_data=tender_data)
    tender_analyzer.filter_and_group_tender_data(
        tender_type=tender_type,
        phase=phase,
        start_year=start_year,
        end_year=end_year,
    )
    tender_analyzer.visualize_tender_data(
        visualize_tender_type=visualize_tender_type, top=top
    )

from sqlalchemy import Column, String, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()


# Model for the "tender" table
class Tender(Base):
    __tablename__ = "tender"
    kode = Column(BigInteger, primary_key=True, autoincrement=False)
    nama_paket = Column(String, name="Nama Paket", nullable=True)
    kl_pd_instansi = Column(String, name="K/L/PD/Instansi Lainnya", nullable=True)
    tahapan = Column(String, nullable=True)
    hps = Column(String, nullable=True)

    # Relationships
    tender_pengumumans = relationship("TenderPengumuman", back_populates="tender")
    tender_pesertas = relationship("TenderPeserta", back_populates="tender")
    tender_pemenangs = relationship("TenderPemenang", back_populates="tender")
    tender_pemenang_berkontraks = relationship(
        "TenderPemenangBerkontrak", back_populates="tender"
    )


# Model for the "tender_pengumuman" table
class TenderPengumuman(Base):
    __tablename__ = "tender_pengumuman"
    kode_tender = Column(
        BigInteger,
        ForeignKey("tender.kode"),
        name="Kode Tender",
        primary_key=True,
        nullable=False,
        autoincrement=False,
    )
    nama_tender = Column(String, name="Nama Tender", nullable=True)
    rencana_umum_pengadaan = Column(
        String, name="Rencana Umum Pengadaan", nullable=True
    )
    uraian_singkat_pekerjaan = Column(
        String, name="Uraian Singkat Pekerjaan", nullable=True
    )
    tanggal_pembuatan = Column(String, name="Tanggal Pembuatan", nullable=True)
    tahap_tender_saat_ini = Column(String, name="Tahap Tender Saat Ini", nullable=True)
    kl_pd_instansi = Column(String, name="K/L/PD/Instansi Lainnya", nullable=True)
    satuan_kerja = Column(String, name="Satuan Kerja", nullable=True)
    jenis_pengadaan = Column(String, name="Jenis Pengadaan", nullable=True)
    metode_pengadaan = Column(String, name="Metode Pengadaan", nullable=True)
    khusus_oap = Column(String, name="Khusus Orang Asli Papua (OAP)", nullable=True)
    tahun_anggaran = Column(String, name="Tahun Anggaran", nullable=True)
    nilai_pagu_paket = Column(String, name="Nilai Pagu Paket", nullable=True)
    nilai_hps_paket = Column(String, name="Nilai HPS Paket", nullable=True)
    jenis_kontrak = Column(String, name="Jenis Kontrak", nullable=True)
    lokasi_pekerjaan = Column(String, name="Lokasi Pekerjaan", nullable=True)
    bobot_teknis = Column(String, name="Bobot Teknis", nullable=True)
    bobot_biaya = Column(String, name="Bobot Biaya", nullable=True)
    syarat_kualifikasi = Column(Text, name="Syarat Kualifikasi", nullable=True)
    peserta_tender = Column(String, name="Peserta Tender", nullable=True)

    # Relationships
    tender = relationship("Tender", back_populates="tender_pengumumans")


# Model for the "tender_peserta" table
class TenderPeserta(Base):
    __tablename__ = "tender_peserta"
    kode_tender = Column(
        BigInteger,
        ForeignKey("tender.kode"),
        name="Kode Tender",
        primary_key=False,
        autoincrement=False,
    )
    no = Column(String, name="No", nullable=True)
    nama_peserta = Column(String, name="Nama Peserta", nullable=True)
    npwp = Column(String, nullable=True)
    harga_penawaran = Column(String, name="Harga Penawaran", nullable=True)
    harga_terkoreksi = Column(String, name="Harga Terkoreksi", nullable=True)

    # Relationships
    tender = relationship("Tender", back_populates="tender_pesertas")

    # Define a composite primary key
    __table_args__ = (
        PrimaryKeyConstraint("Kode Tender", "No", name="composite_tender_peserta_pk"),
    )


# Model for the "tender_pemenang" table
class TenderPemenang(Base):
    __tablename__ = "tender_pemenang"
    kode_tender = Column(
        BigInteger,
        ForeignKey("tender.kode"),
        name="Kode Tender",
        primary_key=True,
        autoincrement=False,
    )
    nama_tender = Column(String, name="Nama Tender", nullable=True)
    jenis_pengadaan = Column(String, name="Jenis Pengadaan", nullable=True)
    kl_pd_instansi = Column(String, name="K/L/PD/Instansi Lainnya", nullable=True)
    satuan_kerja = Column(String, name="Satuan Kerja", nullable=True)
    pagu = Column(String, nullable=True)
    hps = Column(String, nullable=True)
    nama_pemenang = Column(String, name="Nama Pemenang", nullable=True)
    alamat = Column(String, nullable=True)
    npwp = Column(String, nullable=True)
    harga_penawaran = Column(String, name="Harga Penawaran", nullable=True)
    harga_terkoreksi = Column(String, name="Harga Terkoreksi", nullable=True)
    harga_negosiasi = Column(String, name="Harga Negosiasi", nullable=True)

    # Relationships
    tender = relationship("Tender", back_populates="tender_pemenangs")


# Model for the "tender_pemenang_berkontrak" table
class TenderPemenangBerkontrak(Base):
    __tablename__ = "tender_pemenang_berkontrak"
    kode_tender = Column(
        BigInteger,
        ForeignKey("tender.kode"),
        name="Kode Tender",
        primary_key=True,
        autoincrement=False,
    )
    nama_tender = Column(String, name="Nama Tender", nullable=True)
    jenis_pengadaan = Column(String, name="Jenis Pengadaan", nullable=True)
    kl_pd_instansi = Column(String, name="K/L/PD/Instansi Lainnya", nullable=True)
    satuan_kerja = Column(String, name="Satuan Kerja", nullable=True)
    pagu = Column(String, nullable=True)
    hps = Column(String, nullable=True)
    nama_pemenang = Column(String, name="Nama Pemenang", nullable=True)
    alamat = Column(String, nullable=True)
    npwp = Column(String, nullable=True)
    harga_kontrak = Column(String, name="Harga Kontrak", nullable=True)
    nilai_pdn = Column(String, name="Nilai PDN", nullable=True)
    nilai_umk = Column(String, name="Nilai UMK", nullable=True)

    # Relationships
    tender = relationship("Tender", back_populates="tender_pemenang_berkontraks")

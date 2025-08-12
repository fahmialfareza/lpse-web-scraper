import fs from "fs";
import path from "path";
import axios from "axios";

export interface AnalyzeParams {
  data_type?: "tender";
  tender_type?:
    | "Pengadaan Barang"
    | "Pekerjaan Konstruksi"
    | "Jasa Konsultansi Badan Usaha Non Konstruksi"
    | "Jasa Konsultansi Badan Usaha Konstruksi"
    | "Jasa Konsultansi Perorangan Non Konstruksi"
    | "Jasa Konsultansi Perorangan Konstruksi"
    | "Jasa Lainnya"
    | "Pekerjaan Konstruksi Terintegrasi";
  phase?:
    | "Tender Gagal"
    | "Tender Sudah Selesai"
    | "Seleksi Gagal"
    | "Masa Sanggah";
  start_year?: number;
  end_year?: number;
  visualize_tender_type?: "Jumlah Tender" | "Total Harga Penawaran";
  top?: number;
}

export async function fetchAnalyzeData(params: AnalyzeParams) {
  const { data } = await axios.get(
    `${process.env.ANALYZER_URL}/api/v1/analyze`,
    {
      params,
    }
  );
  const analyzeDataImage = process.env.ANALYZER_URL + data.data;

  const imageResponse = await axios.get(analyzeDataImage, {
    responseType: "stream",
  });
  const filename = data.data.split("/").pop() || "analyze.png";
  const filePath = path.join(__dirname, "../public", filename);
  const writer = fs.createWriteStream(filePath);
  imageResponse.data.pipe(writer);
  await new Promise<void>((resolve, reject) => {
    writer.on("finish", () => resolve());
    writer.on("error", reject);
  });

  return "/" + filename;
}

export async function deleteAnalyzeDataImage() {
  await axios.delete(`${process.env.ANALYZER_URL}/delete-pngs`);

  const publicDir = path.join(__dirname, "../public");
  const files = fs.readdirSync(publicDir);
  await Promise.all(
    files
      .filter((file) => file.endsWith(".png"))
      .map(
        (file) =>
          new Promise<void>((resolve, reject) => {
            fs.unlink(path.join(publicDir, file), (err) => {
              if (err) reject(err);
              else resolve();
            });
          })
      )
  );

  return true;
}

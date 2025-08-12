"use client";

import { getAnalyzeData } from "@/services/analyze";
import useStore from "@/zustand";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const TENDER_TYPES = [
  "Pengadaan Barang",
  "Pekerjaan Konstruksi",
  "Jasa Konsultansi Badan Usaha Non Konstruksi",
  "Jasa Konsultansi Badan Usaha Konstruksi",
  "Jasa Konsultansi Perorangan Non Konstruksi",
  "Jasa Konsultansi Perorangan Konstruksi",
  "Jasa Lainnya",
  "Pekerjaan Konstruksi Terintegrasi",
];

const PHASES = [
  "Tender Gagal",
  "Tender Sudah Selesai",
  "Seleksi Gagal",
  "Masa Sanggah",
];

const VISUALIZE_TENDER_TYPES = ["Jumlah Tender", "Total Harga Penawaran"];

export type TFilterState = {
  tender_type?: string;
  phase?: string;
  start_year?: number;
  end_year?: number;
  visualize_tender_type?: string;
};

export default function TenderAnalysis() {
  const router = useRouter();
  const { token } = useStore();

  const currentYear = new Date().getFullYear();
  const [filters, setFilters] = useState<TFilterState>({
    start_year: 2012,
    end_year: currentYear,
    visualize_tender_type: VISUALIZE_TENDER_TYPES[0],
  });
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchImage = async () => {
      setLoading(true);

      try {
        const { data } = await getAnalyzeData(filters, token);
        if (data) {
          setImageUrl(`${process.env.NEXT_PUBLIC_BACKEND_URL}${data}`);
        } else {
          setImageUrl(null);
        }
      } catch {
        setImageUrl(null);
      }
      setLoading(false);
    };
    fetchImage();
  }, [filters, token]);

  const handleChange = (
    e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    setFilters((prev) => ({
      ...prev,
      [name]:
        value === ""
          ? undefined
          : name.includes("year")
          ? Number(value)
          : value,
    }));
  };

  if (!token) {
    router.push("/auth/login");
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-extrabold mb-6 text-center text-gray-200">
        Tender Analysis
      </h2>
      <div className="bg-gray-800 shadow-md rounded-lg p-6 mb-8">
        <div className="flex flex-wrap gap-4 justify-center">
          <select
            name="tender_type"
            value={filters.tender_type || ""}
            onChange={handleChange}
            className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          >
            <option value="">All Tender Types</option>
            {TENDER_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
          <select
            name="phase"
            value={filters.phase || ""}
            onChange={handleChange}
            className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          >
            <option value="">All Phases</option>
            {PHASES.map((phase) => (
              <option key={phase} value={phase}>
                {phase}
              </option>
            ))}
          </select>
          <input
            type="number"
            name="start_year"
            min={2000}
            max={2100}
            value={filters.start_year || ""}
            onChange={handleChange}
            placeholder="Start Year"
            className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-2 w-32 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <input
            type="number"
            name="end_year"
            min={2000}
            max={2100}
            value={filters.end_year || ""}
            onChange={handleChange}
            placeholder="End Year"
            className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-2 w-32 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <select
            name="visualize_tender_type"
            value={filters.visualize_tender_type || ""}
            onChange={handleChange}
            className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          >
            {VISUALIZE_TENDER_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="flex justify-center items-center min-h-[350px] bg-gray-800 border border-gray-700 rounded-lg shadow-md p-6">
        {loading ? (
          <span className="text-blue-400 font-semibold animate-pulse">
            Loading...
          </span>
        ) : imageUrl ? (
          <Image
            src={imageUrl}
            alt="Tender Analysis"
            className="w-full h-auto object-contain rounded-2xl"
            width={800}
            height={600}
            unoptimized
          />
        ) : (
          <span className="text-gray-400">No data available</span>
        )}
      </div>
    </div>
  );
}

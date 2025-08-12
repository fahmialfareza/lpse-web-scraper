import TenderAnalysis from "@/components/TenderAnalysis";
import { clearData } from "@/services/analyze";
import { Metadata } from "next";
import { cookies } from "next/headers";

export type TFilterState = {
  tender_type?: string;
  phase?: string;
  start_year?: number;
  end_year?: number;
  visualize_tender_type?: string;
};

export const metadata: Metadata = {
  title: "Tender Analysis | LPSE Web Scraper",
  description: "Analyze tender data",
};

export default async function TenderAnalysisPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  await clearData(token);

  return <TenderAnalysis />;
}

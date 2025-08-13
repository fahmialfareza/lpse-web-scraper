import { Metadata } from "next";
import TenderAnalysis from "@/components/TenderAnalysis";

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

export default function TenderAnalysisPage() {
  return <TenderAnalysis />;
}

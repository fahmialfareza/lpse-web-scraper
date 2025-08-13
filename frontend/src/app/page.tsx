import { Metadata } from "next";
import TenderAnalysis from "@/components/TenderAnalysis";
import { cookies } from "next/headers";
import { getProfile } from "@/services/auth";
import { redirect } from "next/navigation";

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
  const { status } = await getProfile(token);
  if (status === 401) {
    cookieStore.delete("token");
    redirect("/auth/login");
  }

  return <TenderAnalysis />;
}

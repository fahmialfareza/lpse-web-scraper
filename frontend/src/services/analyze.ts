import { TFilterState } from "@/app/page";
import { redirect } from "next/navigation";
import { logout } from "./auth";

export const getAnalyzeData = async (
  filters: TFilterState,
  token?: string,
  logoutUser?: () => void
) => {
  if (!token) redirect("/auth/login");

  const params = new URLSearchParams();
  if (filters.tender_type) params.append("tender_type", filters.tender_type);
  if (filters.phase) params.append("phase", filters.phase);
  if (filters.start_year)
    params.append("start_year", filters.start_year.toString());
  if (filters.end_year) params.append("end_year", filters.end_year.toString());
  if (filters.visualize_tender_type)
    params.append("visualize_tender_type", filters.visualize_tender_type);

  const url = `${
    process.env.NEXT_PUBLIC_BACKEND_URL
  }/api/analyze?${params.toString()}`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.status === 401) {
    await logout();
    if (logoutUser) {
      logoutUser();
    }
    redirect("/auth/login");
  }

  return response.json();
};

export const clearData = async (token?: string) => {
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/analyze`;

  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  return response.json();
};

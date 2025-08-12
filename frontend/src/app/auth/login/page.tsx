import { Metadata } from "next";
import Login from "@/components/Login";

export const metadata: Metadata = {
  title: "Login | LPSE Web Scraper",
  description: "Login to your account",
};

export default async function LoginPage() {
  return <Login />;
}

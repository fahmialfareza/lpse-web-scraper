import { Metadata } from "next";
import Login from "@/components/Login";
import { cookies } from "next/headers";
import { getProfile } from "@/services/auth";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Login | LPSE Web Scraper",
  description: "Login to your account",
};

export default async function LoginPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  if (token) {
    const { status } = await getProfile(token);
    if (status === 200) {
      redirect("/");
    }
  }

  return <Login token={token} />;
}

"use client";

import { getProfile } from "@/services/auth";
import useStore from "@/zustand";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "react-toastify";

const Navbar = () => {
  const router = useRouter();
  const { token, user, setUser, logout } = useStore();

  useEffect(() => {
    if (token) {
      const fetchProfile = async () => {
        const { data, message } = await getProfile(token);
        if (!data) {
          toast.error(message);
          return;
        }

        setUser(data.user);
      };
      fetchProfile();
    }
  }, [token, setUser]);

  useEffect(() => {
    if (!token) {
      router.push("/auth/login");
    }
  }, [token, router]);

  return (
    <nav className="sticky top-0 z-50 bg-white dark:bg-gray-900 shadow-md transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex-shrink-0">
            <Link
              href="/"
              className="text-2xl font-extrabold text-blue-600 dark:text-blue-400 tracking-tight"
            >
              LPSE Web Scraper
            </Link>
          </div>
          <div className="flex space-x-2 sm:space-x-4">
            <Link
              href="/"
              className="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200
              text-gray-700 dark:text-gray-200
              hover:bg-blue-100 hover:text-blue-700
              dark:hover:bg-blue-900 dark:hover:text-blue-300"
            >
              Home
            </Link>
            {user ? (
              <a
                className="px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200
              bg-gradient-to-r from-blue-500 to-blue-700
              text-white shadow hover:from-blue-600 hover:to-blue-800
              focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                onClick={(e) => {
                  e.preventDefault();

                  logout();
                  router.push("/auth/login");
                }}
              >
                Logout
              </a>
            ) : (
              <Link
                href="/auth/login"
                className="px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200
              bg-gradient-to-r from-blue-500 to-blue-700
              text-white shadow hover:from-blue-600 hover:to-blue-800
              focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
              >
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

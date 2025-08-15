"use client";

import { getProfile, logout } from "@/services/auth";
import useStore from "@/zustand";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "react-toastify";

const Navbar = ({ token: tokenFromCookie }: { token?: string }) => {
  const router = useRouter();
  const { token, user, setUser, logout: logoutUser, setToken } = useStore();

  useEffect(() => {
    if (token) {
      const fetchProfile = async () => {
        const { data, message } = await getProfile(token, logoutUser);
        if (!data) {
          toast.error(message);
          return;
        }

        setUser(data.user);
      };
      fetchProfile();
    }
  }, [token, setUser, logoutUser]);

  useEffect(() => {
    setToken(tokenFromCookie || "");
  }, [tokenFromCookie, setToken]);

  return (
    <nav className="sticky top-0 z-50 bg-white dark:bg-gray-900 shadow-md transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex-shrink-0">
            <Link
              href="/"
              className="text-2xl font-extrabold text-blue-600 dark:text-blue-400 tracking-tight flex items-center gap-2"
            >
              <span className="text-3xl" role="img" aria-label="web">
                🕸️
              </span>
              LPSE Web Scraper
            </Link>
          </div>
          {/* Mobile menu button */}
          <div className="flex sm:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-200 hover:text-blue-700 dark:hover:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-400"
              aria-controls="mobile-menu"
              aria-expanded="false"
              onClick={() => {
                const menu = document.getElementById("mobile-menu");
                if (menu) {
                  menu.classList.toggle("hidden");
                }
              }}
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className="h-6 w-6"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
          {/* Desktop menu */}
          <div className="hidden sm:flex space-x-2 sm:space-x-4">
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
                onClick={async (e) => {
                  e.preventDefault();
                  const message = await logout();
                  if (message === "Logged out") {
                    logoutUser();
                    router.push("/auth/login");
                  }
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
      {/* Mobile menu, show/hide based on menu state. */}
      <div className="sm:hidden hidden" id="mobile-menu">
        <div className="px-2 pt-2 pb-3 space-y-1">
          <Link
            href="/"
            className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-blue-100 hover:text-blue-700 dark:hover:bg-blue-900 dark:hover:text-blue-300"
          >
            Home
          </Link>
          {user ? (
            <a
              className="block px-3 py-2 rounded-md text-base font-semibold bg-gradient-to-r from-blue-500 to-blue-700 text-white shadow hover:from-blue-600 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
              onClick={async (e) => {
                e.preventDefault();
                const message = await logout();
                if (message === "Logged out") {
                  logoutUser();
                  router.push("/auth/login");
                  // Hide menu after logout
                  const menu = document.getElementById("mobile-menu");
                  if (menu) menu.classList.add("hidden");
                }
              }}
            >
              Logout
            </a>
          ) : (
            <Link
              href="/auth/login"
              className="block px-3 py-2 rounded-md text-base font-semibold bg-gradient-to-r from-blue-500 to-blue-700 text-white shadow hover:from-blue-600 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
              onClick={() => {
                // Hide menu after click
                const menu = document.getElementById("mobile-menu");
                if (menu) menu.classList.add("hidden");
              }}
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

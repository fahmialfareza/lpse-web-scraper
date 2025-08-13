"use client";

import { login } from "@/services/auth";
import useStore from "@/zustand";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "react-toastify";

export default function Login() {
  const router = useRouter();
  const { setToken, setUser, user } = useStore();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const { data, message } = await login(username, password);
    if (!data) {
      toast.error(message);
      return;
    }
    setToken(data.token);
    setUser(data.user);

    router.push("/");
  };

  useEffect(() => {
    if (user) {
      router.push("/");
    }
  }, [router, user]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 dark:bg-gradient-to-br dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
      <div className="w-full max-w-md p-8 rounded-xl shadow-2xl bg-white/90 dark:bg-gray-900/90 backdrop-blur-md">
        <h2 className="text-3xl font-bold text-center mb-6 text-gray-800 dark:text-white">
          Welcome Back
        </h2>
        <form className="space-y-5" onSubmit={onSubmit}>
          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 mb-1"
              htmlFor="username"
            >
              Username
            </label>
            <input
              id="username"
              type="username"
              autoComplete="username"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="username"
            />
          </div>
          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 mb-1"
              htmlFor="password"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-white font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            Sign In
          </button>
        </form>
        <div className="mt-6 text-center text-gray-600 dark:text-gray-400 text-sm">
          Don&apos;t have an account?{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}

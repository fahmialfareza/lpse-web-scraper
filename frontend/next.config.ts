import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [new URL("http://localhost:4000/**")],
  },
};

export default nextConfig;

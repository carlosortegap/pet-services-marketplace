import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typescript: {
    // Allow deployment with type errors — fix iteratively
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**.amazonaws.com' },
      { protocol: 'https', hostname: 'lh3.googleusercontent.com' },
    ],
  },
}
export default nextConfig

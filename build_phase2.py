"""
build_phase2.py — PetCare Marketplace · Phase 2 Build Script
============================================================
Writes ALL Phase 2 files in a single pass:

  COMPONENTS
  ├── src/components/shared/Navbar.tsx
  ├── src/components/shared/SearchBar.tsx
  ├── src/components/shared/Footer.tsx
  ├── src/components/providers/ProviderCard.tsx
  ├── src/components/providers/ProviderGrid.tsx
  └── src/components/providers/Hero.tsx   (geolocation + embedded search)

  PAGES
  ├── src/app/page.tsx                    (updated homepage)
  └── src/app/providers/page.tsx          (providers listing page)

  SEED
  └── prisma/seed.ts                      (6 users: 3 owners + 2 vets + 1 walker)

  CONFIG
  └── package.json prisma.seed entry      (ensures `npx prisma db seed` works)

Run:
  cd ~/Desktop/project/pet-services-marketplace
  python3 build_phase2.py
"""

import os
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  ✓  {rel}")


def patch_package_json() -> None:
    pkg_path = ROOT / "package.json"
    if not pkg_path.exists():
        print("  ⚠  package.json not found — skipping seed entry patch")
        return
    pkg = json.loads(pkg_path.read_text())
    # Add prisma.seed if missing
    pkg.setdefault("prisma", {})
    if pkg["prisma"].get("seed") != "ts-node --compiler-options '{\"module\":\"CommonJS\"}' prisma/seed.ts":
        pkg["prisma"]["seed"] = "ts-node --compiler-options '{\"module\":\"CommonJS\"}' prisma/seed.ts"
        pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
        print("  ✓  package.json → prisma.seed entry added")
    else:
        print("  –  package.json prisma.seed already set")


# ─────────────────────────────────────────────────────────────
# FILE CONTENTS
# ─────────────────────────────────────────────────────────────

NAVBAR = '''\
"use client";

import { useState } from "react";
import Link from "next/link";
import { useSession, signOut } from "next-auth/react";
import { Menu, X, PawPrint, ChevronDown } from "lucide-react";

export default function Navbar() {
  const { data: session, status } = useSession();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const dashboardHref =
    session?.user?.role === "PROVIDER" ? "/dashboard/provider" : "/dashboard/owner";

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl text-blue-600">
            <PawPrint className="w-6 h-6" />
            <span>PetCare</span>
          </Link>

          {/* Desktop nav links */}
          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
            <Link href="/providers" className="hover:text-blue-600 transition">Find Providers</Link>
            <Link href="/providers?type=VETERINARIAN" className="hover:text-blue-600 transition">Vets</Link>
            <Link href="/providers?type=PET_WALKER" className="hover:text-blue-600 transition">Walkers</Link>
          </div>

          {/* Auth area */}
          <div className="hidden md:flex items-center gap-3">
            {status === "loading" ? (
              <div className="w-8 h-8 rounded-full bg-gray-200 animate-pulse" />
            ) : session ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition"
                >
                  {session.user?.image ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={session.user.image} alt={session.user.name ?? ""} className="w-8 h-8 rounded-full object-cover" />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold text-sm">
                      {session.user?.name?.[0]?.toUpperCase() ?? "?"}
                    </div>
                  )}
                  <span className="max-w-[120px] truncate">{session.user?.name}</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {userMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 text-sm z-10">
                    <Link href={dashboardHref} className="block px-4 py-2 text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Dashboard</Link>
                    <Link href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Profile</Link>
                    <hr className="my-1 border-gray-100" />
                    <button onClick={() => signOut({ callbackUrl: "/" })} className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50">
                      Sign out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link href="/login" className="text-sm font-medium text-gray-700 hover:text-blue-600 transition">Log in</Link>
                <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-blue-700 transition">Sign up</Link>
              </>
            )}
          </div>

          {/* Mobile hamburger */}
          <button className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-4 py-4 space-y-2">
          <Link href="/providers" className="block py-2 text-gray-700 font-medium" onClick={() => setMobileOpen(false)}>Find Providers</Link>
          <Link href="/providers?type=VETERINARIAN" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Veterinarians</Link>
          <Link href="/providers?type=PET_WALKER" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Pet Walkers</Link>
          <hr className="border-gray-100" />
          {session ? (
            <>
              <Link href={dashboardHref} className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Dashboard</Link>
              <button onClick={() => signOut({ callbackUrl: "/" })} className="block w-full text-left py-2 text-red-600">Sign out</button>
            </>
          ) : (
            <>
              <Link href="/login" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Log in</Link>
              <Link href="/register" className="block py-2 text-blue-600 font-semibold" onClick={() => setMobileOpen(false)}>Sign up free</Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
'''

SEARCHBAR = '''\
"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Search, MapPin } from "lucide-react";

interface SearchBarProps {
  className?: string;
  defaultType?: string;
  defaultRadius?: string;
  defaultQuery?: string;
  onSearch?: (params: { query: string; type: string; radius: string }) => void;
}

export default function SearchBar({
  className = "",
  defaultType = "",
  defaultRadius = "10",
  defaultQuery = "",
  onSearch,
}: SearchBarProps) {
  const router = useRouter();
  const [query, setQuery] = useState(defaultQuery);
  const [type, setType] = useState(defaultType);
  const [radius, setRadius] = useState(defaultRadius);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const params = new URLSearchParams();
    if (query.trim()) params.set("q", query.trim());
    if (type) params.set("type", type);
    if (radius) params.set("radius", radius);
    if (onSearch) {
      onSearch({ query, type, radius });
    } else {
      router.push(`/providers?${params.toString()}`);
    }
  }

  return (
    <form onSubmit={handleSubmit} className={`flex flex-col sm:flex-row gap-2 ${className}`}>
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, breed, service…"
          className="w-full pl-9 pr-4 py-3 rounded-xl border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
        className="px-4 py-3 rounded-xl border border-gray-200 bg-white text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
      >
        <option value="">All providers</option>
        <option value="VETERINARIAN">🏥 Veterinarians</option>
        <option value="PET_WALKER">🦮 Pet walkers</option>
      </select>
      <div className="relative">
        <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <select
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
          className="pl-9 pr-4 py-3 rounded-xl border border-gray-200 bg-white text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
        >
          <option value="5">5 km</option>
          <option value="10">10 km</option>
          <option value="25">25 km</option>
          <option value="50">50 km</option>
        </select>
      </div>
      <button type="submit" className="bg-blue-600 text-white px-6 py-3 rounded-xl text-sm font-semibold hover:bg-blue-700 transition whitespace-nowrap">
        Search
      </button>
    </form>
  );
}
'''

FOOTER = '''\
import Link from "next/link";
import { PawPrint } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-2 text-white font-bold text-lg mb-3">
              <PawPrint className="w-5 h-5 text-blue-400" />
              PetCare
            </Link>
            <p className="text-sm leading-relaxed">
              Connecting pet owners with trusted veterinarians and walkers near you.
            </p>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">Explore</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/providers" className="hover:text-white transition">All Providers</Link></li>
              <li><Link href="/providers?type=VETERINARIAN" className="hover:text-white transition">Veterinarians</Link></li>
              <li><Link href="/providers?type=PET_WALKER" className="hover:text-white transition">Pet Walkers</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">For Providers</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/register?role=provider" className="hover:text-white transition">Join as Provider</Link></li>
              <li><Link href="/dashboard/provider" className="hover:text-white transition">Provider Dashboard</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/privacy" className="hover:text-white transition">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-white transition">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs">
          <p>© {new Date().getFullYear()} PetCare Marketplace. All rights reserved.</p>
          <p>Built with Next.js · Prisma · Vercel</p>
        </div>
      </div>
    </footer>
  );
}
'''

PROVIDER_CARD = '''\
import Link from "next/link";
import { Star, MapPin, Clock, DollarSign } from "lucide-react";

export interface ProviderCardService {
  id: string;
  name: string;
  price: number;
  durationMinutes: number;
}

export interface ProviderCardProps {
  id: string;
  name: string;
  avatarUrl?: string | null;
  type: "VETERINARIAN" | "PET_WALKER";
  bio?: string | null;
  city?: string | null;
  distanceKm?: number | null;
  avgRating?: number | null;
  reviewCount?: number;
  services?: ProviderCardService[];
}

const TYPE_LABEL: Record<string, string> = {
  VETERINARIAN: "🏥 Veterinarian",
  PET_WALKER: "🦮 Pet Walker",
};

const TYPE_COLOR: Record<string, string> = {
  VETERINARIAN: "bg-green-100 text-green-700",
  PET_WALKER: "bg-orange-100 text-orange-700",
};

function Stars({ rating, count }: { rating: number; count?: number }) {
  return (
    <div className="flex items-center gap-1 text-sm">
      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
      <span className="font-semibold text-gray-900">{rating.toFixed(1)}</span>
      {count !== undefined && <span className="text-gray-400">({count})</span>}
    </div>
  );
}

export default function ProviderCard({
  id, name, avatarUrl, type, bio, city, distanceKm, avgRating, reviewCount = 0, services = [],
}: ProviderCardProps) {
  const lowestPrice = services.length ? Math.min(...services.map((s) => s.price)) : null;

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden flex flex-col">
      <div className="p-5 flex items-start gap-4">
        {avatarUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={avatarUrl} alt={name} className="w-16 h-16 rounded-xl object-cover flex-shrink-0" />
        ) : (
          <div className="w-16 h-16 rounded-xl bg-blue-100 flex items-center justify-center text-2xl font-bold text-blue-600 flex-shrink-0">
            {name[0]?.toUpperCase()}
          </div>
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-semibold text-gray-900 text-base leading-tight truncate">{name}</h3>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full whitespace-nowrap flex-shrink-0 ${TYPE_COLOR[type] ?? "bg-gray-100 text-gray-600"}`}>
              {TYPE_LABEL[type] ?? type}
            </span>
          </div>
          {avgRating != null && <div className="mt-1"><Stars rating={avgRating} count={reviewCount} /></div>}
          <div className="flex items-center gap-1 mt-1 text-xs text-gray-500">
            <MapPin className="w-3 h-3" />
            <span className="truncate">{city ?? "Location unavailable"}</span>
            {distanceKm != null && (
              <span className="ml-1 text-blue-600 font-medium">· {distanceKm.toFixed(1)} km</span>
            )}
          </div>
        </div>
      </div>

      {bio && <p className="px-5 text-sm text-gray-500 line-clamp-2 leading-relaxed">{bio}</p>}

      {services.length > 0 && (
        <div className="px-5 mt-3 flex flex-wrap gap-1.5">
          {services.slice(0, 3).map((s) => (
            <span key={s.id} className="flex items-center gap-1 text-xs bg-gray-50 border border-gray-100 rounded-full px-2.5 py-1 text-gray-600">
              <Clock className="w-3 h-3" />{s.name}
            </span>
          ))}
          {services.length > 3 && <span className="text-xs text-gray-400 px-1 py-1">+{services.length - 3} more</span>}
        </div>
      )}

      <div className="mt-auto px-5 py-4 flex items-center justify-between border-t border-gray-50">
        {lowestPrice != null ? (
          <div className="flex items-center gap-1 text-sm text-gray-700">
            <DollarSign className="w-4 h-4 text-green-600" />
            <span>From <strong>${lowestPrice}</strong>/hr</span>
          </div>
        ) : (
          <span className="text-sm text-gray-400">Price on request</span>
        )}
        <Link href={`/providers/${id}`} className="bg-blue-600 text-white text-sm font-semibold px-4 py-2 rounded-full hover:bg-blue-700 transition">
          Book now
        </Link>
      </div>
    </div>
  );
}
'''

PROVIDER_GRID = '''\
import ProviderCard, { ProviderCardProps } from "./ProviderCard";

interface ProviderGridProps {
  providers: ProviderCardProps[];
  loading?: boolean;
}

function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden animate-pulse">
      <div className="p-5 flex items-start gap-4">
        <div className="w-16 h-16 rounded-xl bg-gray-200 flex-shrink-0" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gray-200 rounded w-3/4" />
          <div className="h-3 bg-gray-200 rounded w-1/2" />
          <div className="h-3 bg-gray-200 rounded w-2/3" />
        </div>
      </div>
      <div className="px-5 pb-5">
        <div className="h-3 bg-gray-200 rounded mb-2" />
        <div className="h-3 bg-gray-200 rounded w-5/6" />
      </div>
      <div className="px-5 py-4 border-t border-gray-50 flex justify-between">
        <div className="h-4 bg-gray-200 rounded w-20" />
        <div className="h-8 bg-gray-200 rounded-full w-24" />
      </div>
    </div>
  );
}

export default function ProviderGrid({ providers, loading = false }: ProviderGridProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
      </div>
    );
  }

  if (providers.length === 0) {
    return (
      <div className="text-center py-20 text-gray-500">
        <div className="text-5xl mb-4">🔍</div>
        <h3 className="text-lg font-semibold text-gray-700 mb-1">No providers found</h3>
        <p className="text-sm">Try adjusting your filters or expanding the search radius.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {providers.map((p) => (
        <ProviderCard key={p.id} {...p} />
      ))}
    </div>
  );
}
'''

HERO = '''\
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MapPin, Loader2 } from "lucide-react";
import SearchBar from "@/components/shared/SearchBar";

export default function Hero() {
  const router = useRouter();
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoError, setGeoError] = useState<string | null>(null);

  function handleFindNearMe() {
    if (!navigator.geolocation) {
      setGeoError("Geolocation is not supported by your browser.");
      return;
    }
    setGeoLoading(true);
    setGeoError(null);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        router.push(`/providers?lat=${latitude}&lng=${longitude}&radius=10`);
        setGeoLoading(false);
      },
      () => {
        setGeoError("Could not get your location. Please allow location access.");
        setGeoLoading(false);
      }
    );
  }

  return (
    <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
      {/* Decorative blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-32 -left-16 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28 text-center">
        {/* Badge */}
        <span className="inline-block bg-white/20 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1 rounded-full mb-6 tracking-wide uppercase">
          🐾 Trusted pet care in Mexico City
        </span>

        {/* Headline */}
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-4 drop-shadow">
          Find the best care<br className="hidden sm:block" /> for your pet
        </h1>
        <p className="text-blue-100 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          Book trusted veterinarians and pet walkers near you — verified reviews, instant booking, no hassle.
        </p>

        {/* Search bar */}
        <div className="max-w-3xl mx-auto mb-6">
          <SearchBar className="bg-white rounded-2xl p-3 shadow-2xl" />
        </div>

        {/* Find near me */}
        <button
          onClick={handleFindNearMe}
          disabled={geoLoading}
          className="inline-flex items-center gap-2 text-sm text-blue-100 hover:text-white transition disabled:opacity-60"
        >
          {geoLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <MapPin className="w-4 h-4" />
          )}
          {geoLoading ? "Detecting location…" : "Use my current location"}
        </button>

        {geoError && (
          <p className="mt-2 text-red-300 text-sm">{geoError}</p>
        )}

        {/* Trust badges */}
        <div className="mt-12 flex flex-wrap justify-center gap-6 text-sm text-blue-200">
          <span>✅ Verified providers</span>
          <span>⭐ 4.8 avg rating</span>
          <span>🔒 Secure payments</span>
          <span>📅 Instant booking</span>
        </div>
      </div>
    </section>
  );
}
'''

HOME_PAGE = '''\
import Hero from "@/components/providers/Hero";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen flex flex-col">
        <Hero />

        {/* Feature cards */}
        <section className="bg-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Everything your pet needs
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { icon: "🏥", title: "Veterinarians", desc: "Certified vets for checkups, vaccinations, and emergency care.", href: "/providers?type=VETERINARIAN" },
                { icon: "🦮", title: "Pet Walkers", desc: "Trusted walkers for daily exercise, group sessions, and overnight stays.", href: "/providers?type=PET_WALKER" },
                { icon: "⭐", title: "Verified Reviews", desc: "Real reviews from pet owners so you can book with confidence.", href: "/providers" },
              ].map((f) => (
                <Link
                  key={f.title}
                  href={f.href}
                  className="bg-gray-50 rounded-2xl p-8 text-center hover:shadow-md hover:-translate-y-1 transition-all duration-200 border border-gray-100 group"
                >
                  <div className="text-5xl mb-4">{f.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition">{f.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{f.desc}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="bg-blue-600 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-white text-center">
              {[
                { value: "2,000+", label: "Pet Owners" },
                { value: "250+", label: "Providers" },
                { value: "4.8⭐", label: "Avg Rating" },
                { value: "10K+", label: "Bookings" },
              ].map((s) => (
                <div key={s.label}>
                  <div className="text-4xl font-extrabold">{s.value}</div>
                  <div className="text-blue-200 mt-1 text-sm">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-white py-20 text-center">
          <div className="max-w-2xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Are you a pet care professional?</h2>
            <p className="text-gray-600 mb-8">Join our marketplace, set your own rates, and connect with thousands of pet owners in your area.</p>
            <Link href="/register?role=provider" className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-700 transition inline-block">
              Join as a Provider
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
'''

PROVIDERS_PAGE = '''\
"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import SearchBar from "@/components/shared/SearchBar";
import ProviderGrid from "@/components/providers/ProviderGrid";
import { ProviderCardProps } from "@/components/providers/ProviderCard";

function ProvidersInner() {
  const searchParams = useSearchParams();
  const [providers, setProviders] = useState<ProviderCardProps[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const type = searchParams.get("type") ?? "";
  const radius = searchParams.get("radius") ?? "10";
  const query = searchParams.get("q") ?? "";
  const lat = searchParams.get("lat");
  const lng = searchParams.get("lng");

  useEffect(() => {
    async function fetchProviders() {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (type) params.set("type", type);
        if (radius) params.set("radius", radius);
        if (query) params.set("q", query);
        if (lat) params.set("lat", lat);
        if (lng) params.set("lng", lng);

        const res = await fetch(`/api/providers?${params.toString()}`);
        if (!res.ok) throw new Error("Failed to fetch providers");
        const data = await res.json();

        // Normalise API shape → ProviderCardProps
        const normalised: ProviderCardProps[] = (data.providers ?? data).map((p: {
          id: string;
          user?: { name?: string };
          displayName?: string;
          avatarUrl?: string;
          type: "VETERINARIAN" | "PET_WALKER";
          bio?: string;
          city?: string;
          distanceKm?: number;
          rating?: number;
          reviewCount?: number;
          services?: { id: string; name: string; price: number; durationMinutes: number }[];
        }) => ({
          id: p.id,
          name: p.user?.name ?? p.displayName ?? "Unknown",
          avatarUrl: p.avatarUrl ?? null,
          type: p.type,
          bio: p.bio ?? null,
          city: p.city ?? null,
          distanceKm: p.distanceKm ?? null,
          avgRating: p.rating ?? null,
          reviewCount: p.reviewCount ?? 0,
          services: p.services ?? [],
        }));
        setProviders(normalised);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    }
    fetchProviders();
  }, [type, radius, query, lat, lng]);

  const title =
    type === "VETERINARIAN" ? "Veterinarians" :
    type === "PET_WALKER" ? "Pet Walkers" :
    "All Providers";

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">{title}</h1>
            <SearchBar defaultType={type} defaultRadius={radius} defaultQuery={query} />
          </div>
        </div>

        {/* Results */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {error ? (
            <div className="text-center py-20 text-red-500">
              <p>⚠️ {error}</p>
            </div>
          ) : (
            <>
              {!loading && (
                <p className="text-sm text-gray-500 mb-6">
                  {providers.length} provider{providers.length !== 1 ? "s" : ""} found
                  {radius && ` within ${radius} km`}
                </p>
              )}
              <ProviderGrid providers={providers} loading={loading} />
            </>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}

export default function ProvidersPage() {
  return (
    <Suspense>
      <ProvidersInner />
    </Suspense>
  );
}
'''

SEED = '''\
/**
 * prisma/seed.ts
 * 6 test users: 3 owners + 2 vets + 1 walker
 *
 * Run:  npx prisma db seed
 * Credentials (all):  password = "password123"
 */

import { PrismaClient, UserRole, ProviderType, SubscriptionTier } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱  Seeding database…");

  const hash = await bcrypt.hash("password123", 10);

  // ── OWNERS ────────────────────────────────────────────────
  const owner1 = await prisma.user.upsert({
    where: { email: "sofia.ramirez@test.com" },
    update: {},
    create: {
      email: "sofia.ramirez@test.com",
      name: "Sofía Ramírez",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0001",
      ownerProfile: {
        create: {
          bio: "Dog mom × 2. Always looking for the best care for Luna and Frida.",
          city: "Polanco, CDMX",
          latitude: 19.4326,
          longitude: -99.1332,
          pets: {
            create: [
              { name: "Luna",  species: "dog", breed: "Golden Retriever", age: 3, weight: 28 },
              { name: "Frida", species: "dog", breed: "Chihuahua",        age: 6, weight: 2.5 },
            ],
          },
        },
      },
    },
  });

  const owner2 = await prisma.user.upsert({
    where: { email: "carlos.mendoza@test.com" },
    update: {},
    create: {
      email: "carlos.mendoza@test.com",
      name: "Carlos Mendoza",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0002",
      ownerProfile: {
        create: {
          city: "Roma Norte, CDMX",
          latitude: 19.4195,
          longitude: -99.1585,
          pets: {
            create: [
              { name: "Tobi", species: "cat", breed: "Siamese", age: 2, weight: 4 },
            ],
          },
        },
      },
    },
  });

  const owner3 = await prisma.user.upsert({
    where: { email: "ana.torres@test.com" },
    update: {},
    create: {
      email: "ana.torres@test.com",
      name: "Ana Torres",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0003",
      ownerProfile: {
        create: {
          city: "Condesa, CDMX",
          latitude: 19.4128,
          longitude: -99.1707,
          pets: {
            create: [
              { name: "Max",  species: "dog", breed: "Border Collie", age: 4, weight: 20 },
              { name: "Mimi", species: "rabbit", breed: "Holland Lop", age: 1, weight: 1.8 },
            ],
          },
        },
      },
    },
  });

  console.log(`  ✓  owners: ${owner1.name}, ${owner2.name}, ${owner3.name}`);

  // ── PROVIDERS ─────────────────────────────────────────────
  const vet1 = await prisma.user.upsert({
    where: { email: "dra.garcia@test.com" },
    update: {},
    create: {
      email: "dra.garcia@test.com",
      name: "Dra. María García",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0001",
      providerProfile: {
        create: {
          type: ProviderType.VETERINARIAN,
          displayName: "Dra. María García — Clínica Mascotas Felices",
          bio: "Veterinarian with 12 years of experience. Specialising in small animals, preventive care, and surgery. Fluent Spanish & English.",
          clinicName: "Clínica Mascotas Felices",
          address: "Av. Presidente Masaryk 123",
          city: "Polanco, CDMX",
          latitude: 19.4350,
          longitude: -99.1900,
          serviceRadius: 15,
          hourlyRate: 800,
          isVerified: true,
          isAvailable: true,
          rating: 4.9,
          reviewCount: 87,
          bookingCount: 210,
          specializations: {
            create: [
              { name: "Surgery" },
              { name: "Preventive care" },
              { name: "Dentistry" },
            ],
          },
          services: {
            create: [
              { name: "General Consultation", durationMinutes: 30, price: 400, description: "Full physical exam + diagnosis" },
              { name: "Vaccination", durationMinutes: 20, price: 250, description: "Core vaccines + certificate" },
              { name: "Dental Cleaning", durationMinutes: 60, price: 1200, description: "Under sedation, full oral health check" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 2, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 3, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 4, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 5, startTime: "09:00", endTime: "15:00" },
            ],
          },
        },
      },
    },
  });

  const vet2 = await prisma.user.upsert({
    where: { email: "dr.hernandez@test.com" },
    update: {},
    create: {
      email: "dr.hernandez@test.com",
      name: "Dr. Javier Hernández",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0002",
      providerProfile: {
        create: {
          type: ProviderType.VETERINARIAN,
          displayName: "Dr. Javier Hernández — VetExpress Roma",
          bio: "Emergency vet and exotic animal specialist. 24/7 urgent care available. 8 years experience.",
          clinicName: "VetExpress Roma",
          address: "Calle Orizaba 88",
          city: "Roma Norte, CDMX",
          latitude: 19.4180,
          longitude: -99.1600,
          serviceRadius: 10,
          hourlyRate: 700,
          isVerified: true,
          isAvailable: true,
          rating: 4.7,
          reviewCount: 54,
          bookingCount: 130,
          specializations: {
            create: [
              { name: "Emergency care" },
              { name: "Exotic animals" },
              { name: "Internal medicine" },
            ],
          },
          services: {
            create: [
              { name: "Emergency Consultation", durationMinutes: 45, price: 600, description: "Urgent care, any hour" },
              { name: "General Checkup", durationMinutes: 30, price: 350, description: "Routine wellness exam" },
              { name: "Blood Panel", durationMinutes: 20, price: 500, description: "Full CBC + chemistry" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 2, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 3, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 4, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 5, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 6, startTime: "10:00", endTime: "20:00" },
              { dayOfWeek: 0, startTime: "10:00", endTime: "18:00" },
            ],
          },
        },
      },
    },
  });

  const walker = await prisma.user.upsert({
    where: { email: "diego.walker@test.com" },
    update: {},
    create: {
      email: "diego.walker@test.com",
      name: "Diego López",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0003",
      providerProfile: {
        create: {
          type: ProviderType.PET_WALKER,
          displayName: "Diego López — PawWalks CDMX",
          bio: "Certified dog trainer and walker. Group and private walks in Condesa, Roma, and Polanco parks. GPS-tracked every session.",
          address: "Av. Ámsterdam 45",
          city: "Condesa, CDMX",
          latitude: 19.4100,
          longitude: -99.1750,
          serviceRadius: 8,
          hourlyRate: 200,
          isVerified: true,
          isAvailable: true,
          rating: 4.8,
          reviewCount: 112,
          bookingCount: 350,
          specializations: {
            create: [
              { name: "Dog training" },
              { name: "Group walks" },
              { name: "Puppy socialisation" },
            ],
          },
          services: {
            create: [
              { name: "30-min Solo Walk",   durationMinutes: 30, price: 150,  description: "One-on-one walk, GPS tracked" },
              { name: "60-min Solo Walk",   durationMinutes: 60, price: 250,  description: "Extended solo walk" },
              { name: "Group Walk (4 max)", durationMinutes: 60, price: 120,  description: "Socialise with other friendly dogs" },
              { name: "Puppy Training",     durationMinutes: 45, price: 350,  description: "Basic commands + leash manners" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 2, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 3, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 4, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 5, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 6, startTime: "08:00", endTime: "15:00" },
            ],
          },
        },
      },
    },
  });

  console.log(`  ✓  providers: ${vet1.name}, ${vet2.name}, ${walker.name}`);
  console.log("");
  console.log("🎉  Seed complete!");
  console.log("");
  console.log("  Test credentials (all passwords: password123)");
  console.log("  ┌─ OWNERS ──────────────────────────────────");
  console.log("  │  sofia.ramirez@test.com  (2 dogs)");
  console.log("  │  carlos.mendoza@test.com (1 cat)");
  console.log("  │  ana.torres@test.com     (1 dog + 1 rabbit)");
  console.log("  ├─ PROVIDERS ───────────────────────────────");
  console.log("  │  dra.garcia@test.com     (Vet · Polanco)");
  console.log("  │  dr.hernandez@test.com   (Vet · Roma)");
  console.log("  │  diego.walker@test.com   (Walker · Condesa)");
  console.log("  └───────────────────────────────────────────");
}

main()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(async () => { await prisma.$disconnect(); });
'''

# ─────────────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────────────

def main():
    project = ROOT
    if not (project / "package.json").exists():
        print(f"ERROR: Not a Next.js project root: {project}")
        sys.exit(1)

    print(f"\n🚀  Building Phase 2 — {project}\n")

    print("── COMPONENTS ─────────────────────────────────────────")
    write("src/components/shared/Navbar.tsx",           NAVBAR)
    write("src/components/shared/SearchBar.tsx",        SEARCHBAR)
    write("src/components/shared/Footer.tsx",           FOOTER)
    write("src/components/providers/ProviderCard.tsx",  PROVIDER_CARD)
    write("src/components/providers/ProviderGrid.tsx",  PROVIDER_GRID)
    write("src/components/providers/Hero.tsx",          HERO)

    print("\n── PAGES ───────────────────────────────────────────────")
    write("src/app/page.tsx",               HOME_PAGE)
    write("src/app/providers/page.tsx",     PROVIDERS_PAGE)

    print("\n── SEED ────────────────────────────────────────────────")
    write("prisma/seed.ts", SEED)

    print("\n── CONFIG ──────────────────────────────────────────────")
    patch_package_json()

    print("\n────────────────────────────────────────────────────────")
    print("✅  All Phase 2 files written.\n")
    print("NEXT STEPS:")
    print("  1. Install ts-node (if not already):  npm install -D ts-node")
    print("  2. Run migrations:                    npx prisma migrate dev --name phase2")
    print("  3. Seed the database:                 npx prisma db seed")
    print("  4. Start dev server:                  npm run dev")
    print("  5. Open http://localhost:3000\n")
    print("Test users — password for all: password123")
    print("  Owners   : sofia.ramirez@test.com | carlos.mendoza@test.com | ana.torres@test.com")
    print("  Providers: dra.garcia@test.com | dr.hernandez@test.com | diego.walker@test.com")
    print()


if __name__ == "__main__":
    main()

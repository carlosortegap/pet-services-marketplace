"""
build_phase2b.py — PetCare Marketplace · Phase 2b
===================================================
Writes all missing pages in one pass:

  PAGES
  ├── src/app/(auth)/login/page.tsx
  ├── src/app/(auth)/register/page.tsx
  ├── src/app/(auth)/layout.tsx
  ├── src/app/(dashboard)/owner/page.tsx
  ├── src/app/(dashboard)/provider/page.tsx
  ├── src/app/(dashboard)/layout.tsx
  ├── src/app/providers/[id]/page.tsx
  └── src/app/bookings/[id]/page.tsx

  API
  └── src/app/api/register/route.ts

Run:
  cd ~/Desktop/project/pet-services-marketplace
  python3 build_phase2b.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  ✓  {rel}")


# ─────────────────────────────────────────────────────────────
# AUTH LAYOUT
# ─────────────────────────────────────────────────────────────

AUTH_LAYOUT = '''\
import { PawPrint } from "lucide-react";
import Link from "next/link";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      <div className="p-6">
        <Link href="/" className="inline-flex items-center gap-2 text-blue-600 font-bold text-lg">
          <PawPrint className="w-5 h-5" />
          PetCare
        </Link>
      </div>
      <div className="flex-1 flex items-center justify-center px-4 py-8">
        {children}
      </div>
    </div>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────────

LOGIN_PAGE = '''\
"use client";

import { useState, FormEvent } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Loader2 } from "lucide-react";
import { Suspense } from "react";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "/";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const res = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });
    setLoading(false);
    if (res?.error) {
      setError("Invalid email or password.");
    } else {
      router.push(callbackUrl);
      router.refresh();
    }
  }

  return (
    <div className="bg-white rounded-3xl shadow-xl p-8 w-full max-w-md">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
        <p className="text-gray-500 text-sm mt-1">Sign in to your PetCare account</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold text-sm hover:bg-blue-700 transition disabled:opacity-60 flex items-center justify-center gap-2"
        >
          {loading && <Loader2 className="w-4 h-4 animate-spin" />}
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>

      <div className="mt-6 text-center text-sm text-gray-500">
        Don&apos;t have an account?{" "}
        <Link href="/register" className="text-blue-600 font-semibold hover:underline">
          Sign up free
        </Link>
      </div>

      {/* Test credentials hint */}
      <div className="mt-6 bg-gray-50 rounded-xl p-4 text-xs text-gray-500 space-y-1">
        <p className="font-semibold text-gray-600 mb-2">🧪 Test accounts (password: password123)</p>
        <p>👤 sofia.ramirez@test.com</p>
        <p>🏥 dra.garcia@test.com</p>
        <p>🦮 diego.walker@test.com</p>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# REGISTER PAGE
# ─────────────────────────────────────────────────────────────

REGISTER_PAGE = '''\
"use client";

import { useState, FormEvent, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { signIn } from "next-auth/react";
import Link from "next/link";
import { Loader2 } from "lucide-react";

function RegisterForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const defaultRole = searchParams.get("role") === "provider" ? "PROVIDER" : "OWNER";

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState(defaultRole);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Registration failed");

      // Auto sign-in after registration
      const signInRes = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });
      if (signInRes?.error) throw new Error("Auto sign-in failed — please log in manually.");

      router.push(role === "PROVIDER" ? "/dashboard/provider" : "/dashboard/owner");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-3xl shadow-xl p-8 w-full max-w-md">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
        <p className="text-gray-500 text-sm mt-1">Join the PetCare community</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Role toggle */}
        <div className="grid grid-cols-2 gap-2 bg-gray-100 p-1 rounded-xl">
          {[
            { value: "OWNER", label: "🐾 Pet Owner" },
            { value: "PROVIDER", label: "🏥 Provider" },
          ].map((r) => (
            <button
              key={r.value}
              type="button"
              onClick={() => setRole(r.value)}
              className={`py-2 px-3 rounded-lg text-sm font-medium transition ${
                role === r.value
                  ? "bg-white text-blue-600 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Full name</label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="María García"
            className="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Min. 8 characters"
            className="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold text-sm hover:bg-blue-700 transition disabled:opacity-60 flex items-center justify-center gap-2"
        >
          {loading && <Loader2 className="w-4 h-4 animate-spin" />}
          {loading ? "Creating account…" : "Create account"}
        </button>
      </form>

      <div className="mt-6 text-center text-sm text-gray-500">
        Already have an account?{" "}
        <Link href="/login" className="text-blue-600 font-semibold hover:underline">
          Sign in
        </Link>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense>
      <RegisterForm />
    </Suspense>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# REGISTER API ROUTE
# ─────────────────────────────────────────────────────────────

REGISTER_API = '''\
import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { UserRole } from "@prisma/client";

export async function POST(req: NextRequest) {
  try {
    const { name, email, password, role } = await req.json();

    if (!name || !email || !password) {
      return NextResponse.json({ error: "Name, email and password are required." }, { status: 400 });
    }
    if (password.length < 8) {
      return NextResponse.json({ error: "Password must be at least 8 characters." }, { status: 400 });
    }

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      return NextResponse.json({ error: "An account with this email already exists." }, { status: 409 });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const userRole: UserRole = role === "PROVIDER" ? UserRole.PROVIDER : UserRole.OWNER;

    const user = await prisma.user.create({
      data: {
        name,
        email,
        passwordHash,
        role: userRole,
        ...(userRole === UserRole.OWNER
          ? { ownerProfile: { create: {} } }
          : { providerProfile: {
              create: {
                type: "VETERINARIAN",
                displayName: name,
                address: "",
                city: "",
                latitude: 0,
                longitude: 0,
              },
            }
          }),
      },
    });

    return NextResponse.json({ id: user.id, email: user.email, role: user.role }, { status: 201 });
  } catch (err) {
    console.error("[register]", err);
    return NextResponse.json({ error: "Internal server error." }, { status: 500 });
  }
}
'''

# ─────────────────────────────────────────────────────────────
# DASHBOARD LAYOUT
# ─────────────────────────────────────────────────────────────

DASHBOARD_LAYOUT = '''\
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { redirect } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions);
  if (!session) redirect("/login");
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">{children}</main>
      <Footer />
    </>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# OWNER DASHBOARD
# ─────────────────────────────────────────────────────────────

OWNER_DASHBOARD = '''\
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Calendar, PawPrint, Star, Search } from "lucide-react";

export default async function OwnerDashboard() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) return null;

  const owner = await prisma.ownerProfile.findUnique({
    where: { userId: session.user.id },
    include: {
      pets: true,
      _count: { select: {} },
    },
  });

  const bookings = await prisma.booking.findMany({
    where: { ownerId: session.user.id },
    include: {
      providerProfile: { select: { displayName: true, city: true, type: true } },
      service: { select: { name: true } },
      pet: { select: { name: true } },
    },
    orderBy: { scheduledAt: "desc" },
    take: 5,
  });

  const STATUS_COLOR: Record<string, string> = {
    PENDING: "bg-yellow-100 text-yellow-700",
    CONFIRMED: "bg-blue-100 text-blue-700",
    IN_PROGRESS: "bg-purple-100 text-purple-700",
    COMPLETED: "bg-green-100 text-green-700",
    CANCELLED: "bg-red-100 text-red-700",
    DISPUTED: "bg-orange-100 text-orange-700",
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {session.user.name?.split(" ")[0]} 👋
        </h1>
        <p className="text-gray-500 text-sm mt-1">Manage your pets and bookings</p>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        {[
          { icon: Search, label: "Find a Provider", href: "/providers", color: "bg-blue-600" },
          { icon: Calendar, label: "My Bookings", href: "#bookings", color: "bg-indigo-600" },
          { icon: PawPrint, label: "My Pets", href: "#pets", color: "bg-green-600" },
        ].map((a) => (
          <Link
            key={a.label}
            href={a.href}
            className={`${a.color} text-white rounded-2xl p-5 flex items-center gap-3 hover:opacity-90 transition`}
          >
            <a.icon className="w-5 h-5" />
            <span className="font-semibold text-sm">{a.label}</span>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Pets */}
        <section id="pets">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <PawPrint className="w-5 h-5 text-green-600" /> My Pets
          </h2>
          {owner?.pets.length ? (
            <div className="space-y-3">
              {owner.pets.map((pet) => (
                <div key={pet.id} className="bg-white rounded-xl border border-gray-100 p-4 flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-xl">
                    {pet.species === "dog" ? "🐕" : pet.species === "cat" ? "🐈" : "🐾"}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">{pet.name}</p>
                    <p className="text-xs text-gray-500">{pet.breed ?? pet.species}{pet.age ? ` · ${pet.age}y` : ""}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-gray-400 text-sm">
              No pets added yet
            </div>
          )}
        </section>

        {/* Recent Bookings */}
        <section id="bookings">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-blue-600" /> Recent Bookings
          </h2>
          {bookings.length ? (
            <div className="space-y-3">
              {bookings.map((b) => (
                <Link
                  key={b.id}
                  href={`/bookings/${b.id}`}
                  className="bg-white rounded-xl border border-gray-100 p-4 flex items-start justify-between hover:shadow-sm transition block"
                >
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{b.providerProfile.displayName}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{b.service.name} · {b.pet.name}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {new Date(b.scheduledAt).toLocaleDateString("en-MX", { day: "numeric", month: "short", year: "numeric" })}
                    </p>
                  </div>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[b.status] ?? "bg-gray-100 text-gray-600"}`}>
                    {b.status}
                  </span>
                </Link>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-sm text-gray-400">
              No bookings yet.{" "}
              <Link href="/providers" className="text-blue-600 hover:underline">Find a provider →</Link>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# PROVIDER DASHBOARD
# ─────────────────────────────────────────────────────────────

PROVIDER_DASHBOARD = '''\
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Calendar, Star, DollarSign, Users } from "lucide-react";

export default async function ProviderDashboard() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) return null;

  const profile = await prisma.providerProfile.findUnique({
    where: { userId: session.user.id },
    include: { services: true },
  });

  const bookings = await prisma.booking.findMany({
    where: { providerProfileId: profile?.id },
    include: {
      owner: { select: { name: true } },
      service: { select: { name: true } },
      pet: { select: { name: true, species: true } },
    },
    orderBy: { scheduledAt: "desc" },
    take: 6,
  });

  const totalRevenue = bookings
    .filter((b) => b.status === "COMPLETED")
    .reduce((sum, b) => sum + b.providerPayout, 0);

  const STATUS_COLOR: Record<string, string> = {
    PENDING: "bg-yellow-100 text-yellow-700",
    CONFIRMED: "bg-blue-100 text-blue-700",
    IN_PROGRESS: "bg-purple-100 text-purple-700",
    COMPLETED: "bg-green-100 text-green-700",
    CANCELLED: "bg-red-100 text-red-700",
    DISPUTED: "bg-orange-100 text-orange-700",
  };

  const stats = [
    { icon: Calendar, label: "Total Bookings", value: profile?.bookingCount ?? 0, color: "text-blue-600" },
    { icon: Star, label: "Avg Rating", value: profile ? profile.rating.toFixed(1) + " ⭐" : "—", color: "text-yellow-500" },
    { icon: Users, label: "Reviews", value: profile?.reviewCount ?? 0, color: "text-indigo-600" },
    { icon: DollarSign, label: "Total Earned", value: `$${totalRevenue.toLocaleString()}`, color: "text-green-600" },
  ];

  if (!profile) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center">
        <div className="text-5xl mb-4">🏗️</div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Complete your profile</h1>
        <p className="text-gray-500 mb-6">Set up your provider profile to start accepting bookings.</p>
        <Link href="/profile/setup" className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
          Set up profile
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {profile.displayName}
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            {profile.type === "VETERINARIAN" ? "🏥 Veterinarian" : "🦮 Pet Walker"} · {profile.city}
          </p>
        </div>
        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${profile.isAvailable ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
          {profile.isAvailable ? "● Available" : "○ Unavailable"}
        </span>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-2xl border border-gray-100 p-5 text-center">
            <s.icon className={`w-5 h-5 mx-auto mb-2 ${s.color}`} />
            <div className="text-xl font-bold text-gray-900">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Services */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">My Services</h2>
          {profile.services.length ? (
            <div className="space-y-3">
              {profile.services.map((s) => (
                <div key={s.id} className="bg-white rounded-xl border border-gray-100 p-4 flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{s.name}</p>
                    <p className="text-xs text-gray-500">{s.durationMinutes} min</p>
                  </div>
                  <span className="font-bold text-green-700 text-sm">${s.price}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-gray-400 text-sm">
              No services added yet
            </div>
          )}
        </section>

        {/* Recent bookings */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Bookings</h2>
          {bookings.length ? (
            <div className="space-y-3">
              {bookings.map((b) => (
                <Link
                  key={b.id}
                  href={`/bookings/${b.id}`}
                  className="bg-white rounded-xl border border-gray-100 p-4 flex items-start justify-between hover:shadow-sm transition block"
                >
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{b.owner.name}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{b.service.name} · {b.pet.name}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {new Date(b.scheduledAt).toLocaleDateString("en-MX", { day: "numeric", month: "short" })}
                    </p>
                  </div>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[b.status] ?? "bg-gray-100 text-gray-600"}`}>
                    {b.status}
                  </span>
                </Link>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-sm text-gray-400">
              No bookings yet
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# PROVIDER DETAIL PAGE
# ─────────────────────────────────────────────────────────────

PROVIDER_DETAIL = '''\
import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import { Star, MapPin, Clock, DollarSign, CheckCircle } from "lucide-react";
import Link from "next/link";

interface Props { params: { id: string } }

export default async function ProviderDetailPage({ params }: Props) {
  const profile = await prisma.providerProfile.findUnique({
    where: { id: params.id },
    include: {
      user: { select: { name: true, email: true } },
      services: { where: { isActive: true } },
      specializations: true,
      reviewsReceived: {
        where: { isPublished: true },
        include: { author: { select: { name: true, avatarUrl: true } } },
        orderBy: { createdAt: "desc" },
        take: 5,
      },
    },
  });

  if (!profile) notFound();

  const typeLabel = profile.type === "VETERINARIAN" ? "🏥 Veterinarian" : "🦮 Pet Walker";

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        {/* Hero */}
        <div className="bg-white border-b border-gray-100">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="flex flex-col sm:flex-row items-start gap-6">
              <div className="w-24 h-24 rounded-2xl bg-blue-100 flex items-center justify-center text-4xl font-bold text-blue-600 flex-shrink-0">
                {profile.user.name?.[0]?.toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2 mb-1">
                  <h1 className="text-2xl font-bold text-gray-900">{profile.displayName}</h1>
                  {profile.isVerified && (
                    <span className="flex items-center gap-1 text-xs text-green-700 bg-green-100 px-2 py-0.5 rounded-full font-medium">
                      <CheckCircle className="w-3 h-3" /> Verified
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-500 mb-2">{typeLabel}</p>
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  {profile.rating > 0 && (
                    <span className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <strong>{profile.rating.toFixed(1)}</strong>
                      <span className="text-gray-400">({profile.reviewCount} reviews)</span>
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    {profile.city}
                  </span>
                  {profile.hourlyRate && (
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-4 h-4 text-green-600" />
                      From ${profile.hourlyRate}/hr
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Bio */}
            {profile.bio && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-3">About</h2>
                <p className="text-gray-600 text-sm leading-relaxed">{profile.bio}</p>
              </section>
            )}

            {/* Specializations */}
            {profile.specializations.length > 0 && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-3">Specializations</h2>
                <div className="flex flex-wrap gap-2">
                  {profile.specializations.map((s) => (
                    <span key={s.id} className="bg-blue-50 text-blue-700 text-xs font-medium px-3 py-1 rounded-full">
                      {s.name}
                    </span>
                  ))}
                </div>
              </section>
            )}

            {/* Reviews */}
            {profile.reviewsReceived.length > 0 && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-4">Reviews</h2>
                <div className="space-y-4">
                  {profile.reviewsReceived.map((r) => (
                    <div key={r.id} className="border-b border-gray-50 last:border-0 pb-4 last:pb-0">
                      <div className="flex items-center gap-2 mb-1">
                        <div className="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-600">
                          {r.author.name?.[0]?.toUpperCase()}
                        </div>
                        <span className="text-sm font-medium text-gray-800">{r.author.name}</span>
                        <div className="flex ml-auto">
                          {Array.from({ length: r.rating }).map((_, i) => (
                            <Star key={i} className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                          ))}
                        </div>
                      </div>
                      {r.comment && <p className="text-sm text-gray-600 ml-9">{r.comment}</p>}
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>

          {/* Right column — services + booking CTA */}
          <div className="space-y-4">
            <div className="bg-white rounded-2xl border border-gray-100 p-6 sticky top-20">
              <h2 className="font-semibold text-gray-900 mb-4">Services</h2>
              {profile.services.length ? (
                <div className="space-y-3 mb-6">
                  {profile.services.map((s) => (
                    <div key={s.id} className="flex items-start justify-between gap-2">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{s.name}</p>
                        <p className="text-xs text-gray-400 flex items-center gap-1">
                          <Clock className="w-3 h-3" /> {s.durationMinutes} min
                        </p>
                      </div>
                      <span className="text-sm font-bold text-green-700 whitespace-nowrap">${s.price}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-400 mb-6">No services listed.</p>
              )}
              <Link
                href={`/login?callbackUrl=/providers/${profile.id}`}
                className="w-full bg-blue-600 text-white text-sm font-semibold py-3 rounded-xl hover:bg-blue-700 transition text-center block"
              >
                Book appointment
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# BOOKING DETAIL PAGE
# ─────────────────────────────────────────────────────────────

BOOKING_DETAIL = '''\
import { prisma } from "@/lib/prisma";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { notFound, redirect } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";
import { Calendar, Clock, DollarSign, MapPin } from "lucide-react";

interface Props { params: { id: string } }

const STATUS_COLOR: Record<string, string> = {
  PENDING: "bg-yellow-100 text-yellow-700",
  CONFIRMED: "bg-blue-100 text-blue-700",
  IN_PROGRESS: "bg-purple-100 text-purple-700",
  COMPLETED: "bg-green-100 text-green-700",
  CANCELLED: "bg-red-100 text-red-700",
  DISPUTED: "bg-orange-100 text-orange-700",
};

export default async function BookingDetailPage({ params }: Props) {
  const session = await getServerSession(authOptions);
  if (!session) redirect("/login");

  const booking = await prisma.booking.findUnique({
    where: { id: params.id },
    include: {
      owner: { select: { name: true, email: true } },
      providerProfile: { select: { displayName: true, city: true, type: true } },
      service: true,
      pet: true,
    },
  });

  if (!booking) notFound();

  // Only owner or the provider can view
  const isOwner = booking.ownerId === session.user.id;
  const providerUser = await prisma.providerProfile.findUnique({
    where: { id: booking.providerProfileId },
    select: { userId: true },
  });
  const isProvider = providerUser?.userId === session.user.id;
  if (!isOwner && !isProvider) redirect("/");

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
            {/* Header */}
            <div className="bg-blue-600 px-6 py-6 text-white">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-blue-200 text-xs mb-1">Booking #{booking.id.slice(-8).toUpperCase()}</p>
                  <h1 className="text-xl font-bold">{booking.service.name}</h1>
                  <p className="text-blue-100 text-sm mt-1">{booking.providerProfile.displayName}</p>
                </div>
                <span className={`text-xs font-semibold px-3 py-1 rounded-full ${STATUS_COLOR[booking.status] ?? "bg-gray-100 text-gray-600"}`}>
                  {booking.status}
                </span>
              </div>
            </div>

            {/* Details */}
            <div className="p-6 space-y-5">
              <Row icon={Calendar} label="Date & Time" value={new Date(booking.scheduledAt).toLocaleString("en-MX", { dateStyle: "full", timeStyle: "short" })} />
              <Row icon={Clock} label="Duration" value={`${booking.durationMinutes} minutes`} />
              <Row icon={MapPin} label="Location" value={booking.providerProfile.city} />
              <Row icon={DollarSign} label="Total" value={`$${booking.totalAmount.toLocaleString()} MXN`} />

              <hr className="border-gray-100" />

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-gray-50 rounded-xl p-4">
                  <p className="text-xs text-gray-400 mb-1">Pet</p>
                  <p className="font-semibold text-gray-800">{booking.pet.name}</p>
                  <p className="text-xs text-gray-500">{booking.pet.breed ?? booking.pet.species}</p>
                </div>
                <div className="bg-gray-50 rounded-xl p-4">
                  <p className="text-xs text-gray-400 mb-1">Owner</p>
                  <p className="font-semibold text-gray-800">{booking.owner.name}</p>
                  <p className="text-xs text-gray-500">{booking.owner.email}</p>
                </div>
              </div>

              {booking.notes && (
                <div className="bg-blue-50 rounded-xl p-4 text-sm text-blue-800">
                  <p className="text-xs text-blue-400 mb-1">Notes</p>
                  {booking.notes}
                </div>
              )}
            </div>

            <div className="px-6 pb-6">
              <Link
                href={isOwner ? "/dashboard/owner" : "/dashboard/provider"}
                className="block w-full text-center bg-gray-900 text-white py-3 rounded-xl font-semibold text-sm hover:bg-gray-700 transition"
              >
                ← Back to dashboard
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

function Row({ icon: Icon, label, value }: { icon: React.ElementType; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
        <Icon className="w-4 h-4 text-gray-500" />
      </div>
      <div>
        <p className="text-xs text-gray-400">{label}</p>
        <p className="font-medium text-gray-800">{value}</p>
      </div>
    </div>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────────────

def main():
    project = ROOT
    if not (project / "package.json").exists():
        print(f"ERROR: Not a Next.js project root: {project}")
        sys.exit(1)

    print(f"\n🚀  Building Phase 2b (missing pages) — {project}\n")

    print("── AUTH PAGES ──────────────────────────────────────────")
    write("src/app/(auth)/layout.tsx",          AUTH_LAYOUT)
    write("src/app/(auth)/login/page.tsx",       LOGIN_PAGE)
    write("src/app/(auth)/register/page.tsx",    REGISTER_PAGE)

    print("\n── API ─────────────────────────────────────────────────")
    write("src/app/api/register/route.ts",       REGISTER_API)

    print("\n── DASHBOARD PAGES ─────────────────────────────────────")
    write("src/app/(dashboard)/layout.tsx",           DASHBOARD_LAYOUT)
    write("src/app/(dashboard)/owner/page.tsx",        OWNER_DASHBOARD)
    write("src/app/(dashboard)/provider/page.tsx",     PROVIDER_DASHBOARD)

    print("\n── DETAIL PAGES ────────────────────────────────────────")
    write("src/app/providers/[id]/page.tsx",    PROVIDER_DETAIL)
    write("src/app/bookings/[id]/page.tsx",     BOOKING_DETAIL)

    print("\n────────────────────────────────────────────────────────")
    print("✅  All pages written. Dev server will hot-reload.\n")
    print("Pages now live:")
    print("  /login                 — sign in")
    print("  /register              — sign up (owner or provider)")
    print("  /register?role=provider — join as provider")
    print("  /dashboard/owner       — owner dashboard (auth required)")
    print("  /dashboard/provider    — provider dashboard (auth required)")
    print("  /providers/[id]        — provider detail + book CTA")
    print("  /bookings/[id]         — booking detail (auth required)")
    print()


if __name__ == "__main__":
    main()

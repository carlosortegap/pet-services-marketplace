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

          <Link href="/" className="flex items-center gap-2 font-bold text-xl text-blue-600">
            <PawPrint className="w-6 h-6" />
            <span>PetCare</span>
          </Link>

          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
            <Link href="/providers" className="hover:text-blue-600 transition">Buscar</Link>
            <Link href="/providers?type=VETERINARIAN" className="hover:text-blue-600 transition">Veterinarios</Link>
            <Link href="/providers?type=PET_WALKER" className="hover:text-blue-600 transition">Paseadores</Link>
            <Link href="/providers/map" className="hover:text-blue-600 transition">🗺️ Mapa</Link>
            <Link href="/about" className="hover:text-blue-600 transition">¿Qué hacemos?</Link>
          </div>

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
                    <Link href={dashboardHref} className="block px-4 py-2 text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Panel de control</Link>
                    <Link href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Mi perfil</Link>
                    <hr className="my-1 border-gray-100" />
                    <button onClick={() => signOut({ callbackUrl: "/" })} className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50">
                      Cerrar sesión
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link href="/login" className="text-sm font-medium text-gray-700 hover:text-blue-600 transition">Iniciar sesión</Link>
                <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-blue-700 transition">Registrarse</Link>
              </>
            )}
          </div>

          <button className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-4 py-4 space-y-2">
          <Link href="/providers" className="block py-2 text-gray-700 font-medium" onClick={() => setMobileOpen(false)}>Buscar Proveedores</Link>
          <Link href="/providers?type=VETERINARIAN" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Veterinarios</Link>
          <Link href="/providers?type=PET_WALKER" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Paseadores</Link>
          <Link href="/providers/map" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>🗺️ Mapa de clínicas</Link>
          <Link href="/about" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>¿Qué hacemos?</Link>
          <hr className="border-gray-100" />
          {session ? (
            <>
              <Link href={dashboardHref} className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Panel de control</Link>
              <button onClick={() => signOut({ callbackUrl: "/" })} className="block w-full text-left py-2 text-red-600">Cerrar sesión</button>
            </>
          ) : (
            <>
              <Link href="/login" className="block py-2 text-gray-700" onClick={() => setMobileOpen(false)}>Iniciar sesión</Link>
              <Link href="/register" className="block py-2 text-blue-600 font-semibold" onClick={() => setMobileOpen(false)}>Registrarse gratis</Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}

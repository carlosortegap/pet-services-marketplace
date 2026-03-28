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

  const type   = searchParams.get("type") ?? "";
  const radius = searchParams.get("radius") ?? "10";
  const query  = searchParams.get("q") ?? "";
  const lat    = searchParams.get("lat");
  const lng    = searchParams.get("lng");

  useEffect(() => {
    async function fetchProviders() {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (type)   params.set("type", type);
        if (radius) params.set("radius", radius);
        if (query)  params.set("query", query);
        if (lat)    params.set("lat", lat);
        if (lng)    params.set("lng", lng);

        const res = await fetch(`/api/providers?${params.toString()}`);
        if (!res.ok) throw new Error("Error al cargar proveedores");
        const data = await res.json();

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
          name: p.user?.name ?? p.displayName ?? "Sin nombre",
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
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    }
    fetchProviders();
  }, [type, radius, query, lat, lng]);

  const title =
    type === "VETERINARIAN" ? "Veterinarios" :
    type === "PET_WALKER"   ? "Paseadores" :
    "Todos los proveedores";

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        <div className="bg-white border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">{title}</h1>
            <SearchBar defaultType={type} defaultRadius={radius} defaultQuery={query} />
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {error ? (
            <div className="text-center py-20 text-red-500">⚠️ {error}</div>
          ) : (
            <>
              {!loading && (
                <p className="text-sm text-gray-500 mb-6">
                  {providers.length} proveedor{providers.length !== 1 ? "es" : ""} encontrado{providers.length !== 1 ? "s" : ""}
                  {radius && ` en un radio de ${radius} km`}
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
  return <Suspense><ProvidersInner /></Suspense>;
}

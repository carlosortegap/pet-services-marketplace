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
      setGeoError("Tu navegador no soporta geolocalización.");
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
        setGeoError("No se pudo obtener tu ubicación. Permite el acceso a la ubicación.");
        setGeoLoading(false);
      }
    );
  }

  return (
    <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-32 -left-16 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28 text-center">
        <span className="inline-block bg-white/20 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1 rounded-full mb-6 tracking-wide uppercase">
          🐾 Cuidado de mascotas de confianza en CDMX
        </span>

        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-4 drop-shadow">
          Encuentra el mejor cuidado<br className="hidden sm:block" /> para tu mascota
        </h1>
        <p className="text-blue-100 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          Agenda con veterinarios y paseadores de confianza cerca de ti — reseñas verificadas, reserva inmediata, sin complicaciones.
        </p>

        <div className="max-w-3xl mx-auto mb-6">
          <SearchBar className="bg-white rounded-2xl p-3 shadow-2xl" />
        </div>

        <button
          onClick={handleFindNearMe}
          disabled={geoLoading}
          className="inline-flex items-center gap-2 text-sm text-blue-100 hover:text-white transition disabled:opacity-60"
        >
          {geoLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <MapPin className="w-4 h-4" />}
          {geoLoading ? "Detectando ubicación…" : "Usar mi ubicación actual"}
        </button>

        {geoError && <p className="mt-2 text-red-300 text-sm">{geoError}</p>}

        <div className="mt-12 flex flex-wrap justify-center gap-6 text-sm text-blue-200">
          <span>✅ Proveedores verificados</span>
          <span>⭐ 4.8 calificación promedio</span>
          <span>🔒 Pagos seguros</span>
          <span>📅 Reserva inmediata</span>
        </div>
      </div>
    </section>
  );
}

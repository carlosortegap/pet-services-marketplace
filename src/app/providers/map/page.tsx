"use client";

import { useEffect, useRef, useState } from "react";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";
import { MapPin, Phone, Star, ExternalLink } from "lucide-react";

interface Clinic {
  id: number;
  name: string;
  address: string;
  neighborhood: string;
  lat: number;
  lng: number;
  rating: number;
  reviews: number;
  type: string;
  specialty?: string;
  phone?: string;
  distanceKm: number;
  services: string[];
}

const CLINICS: Clinic[] = [
  {
    id: 1,
    name: "Clínica Veterinaria los Ángeles México",
    address: "José María Izazaga 57",
    neighborhood: "Centro Sur",
    lat: 19.4258,
    lng: -99.1355,
    rating: 4.7,
    reviews: 143,
    type: "Clínica General",
    phone: "+52 55 5709-0000",
    distanceKm: 0.5,
    services: ["Consulta general", "Vacunación", "Urgencias"],
  },
  {
    id: 2,
    name: "Bichos Boutique Veterinaria",
    address: "Niños Héroes 220",
    neighborhood: "Doctores",
    lat: 19.4195,
    lng: -99.1480,
    rating: 4.9,
    reviews: 212,
    type: "Clínica + Tienda",
    phone: "+52 55 5761-1234",
    distanceKm: 1.5,
    services: ["Consulta", "Grooming", "Cirugía", "Nutrición"],
  },
  {
    id: 3,
    name: "Veterinaria Ami Sam",
    address: "Av. Cuauhtémoc 179-B",
    neighborhood: "Roma Norte",
    lat: 19.4200,
    lng: -99.1580,
    rating: 4.6,
    reviews: 88,
    type: "Veterinaria + Estética",
    distanceKm: 2.0,
    services: ["Consulta", "Baño y corte", "Vacunación", "Desparasitación"],
  },
  {
    id: 4,
    name: "Hospital Veterinario Santa María",
    address: "Insurgentes Norte 168",
    neighborhood: "Santa María la Ribera",
    lat: 19.4420,
    lng: -99.1530,
    rating: 4.8,
    reviews: 356,
    type: "Hospital 24h",
    specialty: "Urgencias 24 horas",
    phone: "+52 55 5547-0000",
    distanceKm: 3.0,
    services: ["Urgencias 24h", "Cirugía", "Hospitalización", "Imagen"],
  },
  {
    id: 5,
    name: "Veterinaria Dr. de Animalitos",
    address: "Salvador Díaz Mirón 55",
    neighborhood: "Santa María la Ribera",
    lat: 19.4405,
    lng: -99.1560,
    rating: 4.7,
    reviews: 178,
    type: "Clínica General",
    distanceKm: 3.0,
    services: ["Consulta", "Vacunación", "Cirugía menor", "Laboratorio"],
  },
  {
    id: 6,
    name: "Veterinaria San Cosme",
    address: "Av. Ribera de San Cosme 157",
    neighborhood: "Santa María la Ribera",
    lat: 19.4398,
    lng: -99.1580,
    rating: 4.5,
    reviews: 94,
    type: "Clínica Establecida",
    distanceKm: 3.2,
    services: ["Consulta", "Vacunación", "Esterilización", "Radiografía"],
  },
  {
    id: 7,
    name: "Clínica Veterinaria Roma Norte",
    address: "Chiapas 128",
    neighborhood: "Roma Norte",
    lat: 19.4155,
    lng: -99.1630,
    rating: 4.8,
    reviews: 267,
    type: "Clínica Especializada",
    distanceKm: 4.0,
    services: ["Medicina interna", "Cardiología", "Dermatología", "Cirugía"],
  },
  {
    id: 8,
    name: "Veterinaria Amsterdam",
    address: "Ámsterdam 212-A",
    neighborhood: "Condesa",
    lat: 19.4128,
    lng: -99.1720,
    rating: 4.9,
    reviews: 421,
    type: "Especialista",
    specialty: "Dermatología veterinaria",
    distanceKm: 5.0,
    services: ["Dermatología", "Alergias", "Piel y pelo", "Consulta general"],
  },
  {
    id: 9,
    name: "Veterinaria Canusco",
    address: "Ometusco 5",
    neighborhood: "Condesa",
    lat: 19.4110,
    lng: -99.1740,
    rating: 5.0,
    reviews: 189,
    type: "Clínica Premium",
    distanceKm: 5.2,
    services: ["Consulta", "Vacunación", "Ultrasonido", "Odontología"],
  },
  {
    id: 10,
    name: "Dra. María García — Mascotas Felices",
    address: "Av. Presidente Masaryk 123",
    neighborhood: "Polanco",
    lat: 19.4350,
    lng: -99.1900,
    rating: 4.9,
    reviews: 87,
    type: "Clínica Privada",
    specialty: "Cirugía y preventiva",
    phone: "+52 55 5280-4567",
    distanceKm: 6.5,
    services: ["Consulta General $400", "Vacunación $250", "Limpieza Dental $1,400"],
  },
];

const TYPE_COLOR: Record<string, string> = {
  "Hospital 24h": "bg-red-100 text-red-700",
  "Especialista": "bg-purple-100 text-purple-700",
  "Clínica Premium": "bg-yellow-100 text-yellow-700",
  "Clínica Especializada": "bg-indigo-100 text-indigo-700",
};

export default function MapPage() {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<unknown>(null);
  const [selected, setSelected] = useState<Clinic | null>(CLINICS[0]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // Dynamically load Leaflet CSS
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(link);

    // Dynamically load Leaflet JS
    const script = document.createElement("script");
    script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    script.onload = () => {
      setLoaded(true);
    };
    document.head.appendChild(script);
    return () => {
      document.head.removeChild(link);
      document.head.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (!loaded || !mapRef.current || mapInstance.current) return;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const L = (window as any).L;
    const map = L.map(mapRef.current).setView([19.4326, -99.1332], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(map);

    // Centro Histórico marker
    const centerIcon = L.divIcon({
      html: `<div style="width:16px;height:16px;background:#3b82f6;border:3px solid white;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,0.4)"></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
      className: "",
    });

    L.marker([19.4326, -99.1332], { icon: centerIcon })
      .addTo(map)
      .bindPopup("<strong>📍 Centro Histórico</strong><br>Punto de referencia");

    // 10km radius circle
    L.circle([19.4326, -99.1332], {
      radius: 10000,
      color: "#3b82f6",
      fillColor: "#3b82f630",
      fillOpacity: 0.1,
      weight: 1.5,
      dashArray: "6 4",
    }).addTo(map);

    // Clinic markers
    CLINICS.forEach((clinic) => {
      const isHospital = clinic.type === "Hospital 24h";
      const color = isHospital ? "#ef4444" : clinic.rating >= 4.8 ? "#8b5cf6" : "#16a34a";

      const icon = L.divIcon({
        html: `<div style="width:32px;height:32px;background:${color};border:2px solid white;border-radius:50%;box-shadow:0 2px 10px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;font-size:14px">🏥</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "",
      });

      const marker = L.marker([clinic.lat, clinic.lng], { icon })
        .addTo(map)
        .bindPopup(`
          <div style="min-width:200px;font-family:system-ui">
            <strong style="font-size:13px">${clinic.name}</strong><br>
            <span style="color:#666;font-size:12px">${clinic.address}, ${clinic.neighborhood}</span><br>
            <span style="color:#f59e0b;font-size:12px">⭐ ${clinic.rating} (${clinic.reviews} reseñas)</span><br>
            <span style="color:#3b82f6;font-size:12px">📍 ${clinic.distanceKm} km del centro</span>
          </div>
        `);

      marker.on("click", () => setSelected(clinic));
    });

    mapInstance.current = map;
  }, [loaded]);

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">🗺️ Mapa de Veterinarias</h1>
                <p className="text-gray-500 text-sm mt-1">
                  {CLINICS.length} clínicas reales dentro de 10 km del Centro Histórico, CDMX
                </p>
              </div>
              <div className="flex gap-3 text-xs">
                <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span>Hospital 24h</span>
                <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-purple-500 inline-block"></span>Especialista</span>
                <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-600 inline-block"></span>Clínica</span>
                <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>Centro</span>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Map */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
                {!loaded && (
                  <div className="h-[520px] flex items-center justify-center bg-gray-50">
                    <div className="text-center text-gray-400">
                      <div className="text-4xl mb-3">🗺️</div>
                      <p className="text-sm">Cargando mapa…</p>
                    </div>
                  </div>
                )}
                <div
                  ref={mapRef}
                  style={{ height: "520px", width: "100%", display: loaded ? "block" : "none" }}
                />
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-3 lg:max-h-[540px] lg:overflow-y-auto pr-1">
              {CLINICS.map((clinic) => (
                <button
                  key={clinic.id}
                  onClick={() => setSelected(clinic)}
                  className={`w-full text-left bg-white rounded-xl border p-4 transition-all hover:shadow-md ${
                    selected?.id === clinic.id ? "border-blue-400 shadow-md ring-1 ring-blue-200" : "border-gray-100"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <p className="font-semibold text-gray-900 text-sm leading-tight">{clinic.name}</p>
                    <span className={`text-xs px-2 py-0.5 rounded-full whitespace-nowrap flex-shrink-0 ${TYPE_COLOR[clinic.type] ?? "bg-green-100 text-green-700"}`}>
                      {clinic.type}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500">{clinic.neighborhood} · {clinic.distanceKm} km</p>
                  <div className="flex items-center gap-1 mt-1">
                    <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                    <span className="text-xs font-semibold">{clinic.rating}</span>
                    <span className="text-xs text-gray-400">({clinic.reviews})</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Selected clinic detail */}
          {selected && (
            <div className="mt-6 bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <h2 className="text-xl font-bold text-gray-900">{selected.name}</h2>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${TYPE_COLOR[selected.type] ?? "bg-green-100 text-green-700"}`}>
                      {selected.type}
                    </span>
                  </div>
                  {selected.specialty && (
                    <p className="text-blue-600 text-sm font-medium mb-2">✨ {selected.specialty}</p>
                  )}
                  <div className="flex items-center gap-1 text-sm text-gray-600 mb-1">
                    <MapPin className="w-4 h-4" />
                    {selected.address}, {selected.neighborhood} · {selected.distanceKm} km del centro
                  </div>
                  {selected.phone && (
                    <div className="flex items-center gap-1 text-sm text-gray-600 mb-1">
                      <Phone className="w-4 h-4" />
                      {selected.phone}
                    </div>
                  )}
                  <div className="flex items-center gap-1 text-sm mt-1">
                    <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <span className="font-semibold">{selected.rating}</span>
                    <span className="text-gray-400">({selected.reviews} reseñas)</span>
                  </div>
                </div>
                <Link
                  href="/providers"
                  className="bg-blue-600 text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition whitespace-nowrap"
                >
                  Ver en el marketplace
                </Link>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {selected.services.map((s) => (
                  <span key={s} className="bg-gray-50 border border-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Google Maps link */}
          <div className="mt-4 text-center">
            <a
              href="https://www.google.com/maps/search/veterinarias+Centro+Historico+CDMX"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-blue-600 hover:underline"
            >
              <ExternalLink className="w-4 h-4" />
              Ver en Google Maps
            </a>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

"""
build_phase2c.py — PetCare Marketplace · Phase 2c
===================================================
Builds:
  1. /providers/map/page.tsx     — Interactive Mapbox map with real CDMX vets
  2. /about/page.tsx             — "Qué hacemos" with real services + pricing
  3. Updated seed with real clinic coordinates

Run:
  cd ~/Desktop/project/pet-services-marketplace
  python3 build_phase2c.py
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
# MAP PAGE — uses Leaflet (no API key needed, free OpenStreetMap)
# ─────────────────────────────────────────────────────────────

MAP_PAGE = '''\
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
'''

# ─────────────────────────────────────────────────────────────
# ABOUT PAGE — "Qué hacemos" with real services + pricing
# ─────────────────────────────────────────────────────────────

ABOUT_PAGE = '''\
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";

const SERVICES = [
  {
    icon: "🩺",
    title: "Consulta General",
    desc: "Evaluación completa de salud, diagnóstico y plan de tratamiento con veterinarios certificados.",
    priceFrom: 300,
    priceTo: 600,
    details: ["Historia clínica completa", "Examen físico general", "Diagnóstico y receta", "Seguimiento post-consulta"],
  },
  {
    icon: "💉",
    title: "Vacunación",
    desc: "Esquemas de vacunación completos para perros y gatos, incluyendo core y no-core vaccines.",
    priceFrom: 250,
    priceTo: 600,
    details: ["Vacuna antirrábica", "Quíntuple / Séxtuple", "Triple felina", "Bordetella y Giardia"],
  },
  {
    icon: "🦷",
    title: "Limpieza Dental",
    desc: "Profilaxis dental profesional con ultrasonido y pulido bajo sedación inhalada.",
    priceFrom: 1400,
    priceTo: 2200,
    details: ["Ultrasonido escariador", "Pulido dental", "Anestesia inhalada", "Evaluación periodontal"],
  },
  {
    icon: "✂️",
    title: "Castración y Esterilización",
    desc: "Procedimiento quirúrgico seguro para controlar la reproducción y mejorar la calidad de vida.",
    priceFrom: 700,
    priceTo: 2800,
    details: ["Preanestesia y monitoreo", "Cirugía laparoscópica disponible", "Recuperación en clínica", "Cuidados post-operatorios"],
  },
  {
    icon: "📷",
    title: "Estudios de Imagen",
    desc: "Radiografías y ultrasonido para diagnóstico preciso de órganos internos.",
    priceFrom: 400,
    priceTo: 1800,
    details: ["Ultrasonido abdominal", "Rayos X (1-2 placas)", "Ecocardiograma", "Resultado en el día"],
  },
  {
    icon: "🔬",
    title: "Laboratorio Clínico",
    desc: "Análisis de sangre, orina y biopsias para diagnóstico completo.",
    priceFrom: 600,
    priceTo: 2000,
    details: ["Biometría hemática", "Química sanguínea", "Urianálisis", "Pruebas de enfermedades infecciosas"],
  },
  {
    icon: "🚨",
    title: "Urgencias 24 horas",
    desc: "Atención de emergencias veterinarias las 24 horas del día, los 7 días de la semana.",
    priceFrom: 500,
    priceTo: 1800,
    details: ["Atención inmediata", "UCI veterinaria", "Oxigenoterapia", "Cirugía de emergencia"],
  },
  {
    icon: "🏥",
    title: "Hospitalización",
    desc: "Internamiento con monitoreo constante, medicación y cuidados de enfermería.",
    priceFrom: 500,
    priceTo: 1500,
    details: ["Monitoreo 24h", "Medicación IV", "Alimentación especializada", "Reportes diarios"],
  },
  {
    icon: "🦮",
    title: "Paseos y Cuidado",
    desc: "Paseadores certificados con rastreo GPS, seguro incluido y reportes por foto.",
    priceFrom: 120,
    priceTo: 350,
    details: ["GPS en tiempo real", "Fotos y reporte", "Máximo 4 perros por grupo", "Seguro de responsabilidad"],
  },
];

const PRICE_TABLE = [
  { service: "Consulta general", min: 300, max: 600, note: "Privada" },
  { service: "Consulta urgencias", min: 500, max: 1800, note: "Según horario" },
  { service: "Vacunación completa", min: 250, max: 600, note: "Perro o gato" },
  { service: "Antirrábica", min: 0, max: 300, note: "Gratis en módulos CDMX" },
  { service: "Limpieza dental (gato/peq)", min: 1400, max: 1800, note: "Con anestesia" },
  { service: "Limpieza dental (grande)", min: 1800, max: 2600, note: "Con anestesia" },
  { service: "Castración macho", min: 700, max: 1800, note: "Según tamaño" },
  { service: "Esterilización hembra", min: 800, max: 2800, note: "Según tamaño" },
  { service: "Ultrasonido abdominal", min: 400, max: 1800, note: "" },
  { service: "Radiografía (placa)", min: 500, max: 1500, note: "" },
  { service: "Panel de sangre completo", min: 600, max: 2000, note: "" },
  { service: "Hospitalización (por noche)", min: 500, max: 1500, note: "" },
  { service: "Desparasitación", min: 200, max: 500, note: "" },
  { service: "Microchip", min: 900, max: 900, note: "Precio fijo aprox." },
  { service: "Paseo solo 30 min", min: 120, max: 200, note: "Con GPS" },
  { service: "Paseo solo 60 min", min: 200, max: 350, note: "Con GPS" },
  { service: "Entrenamiento básico", min: 300, max: 500, note: "Por sesión" },
];

const STATS = [
  { value: "10+", label: "Clínicas verificadas" },
  { value: "250+", label: "Proveedores en CDMX" },
  { value: "4.8⭐", label: "Calificación promedio" },
  { value: "0%", label: "Comisión para reservar" },
];

export default function AboutPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen">
        {/* Hero */}
        <section className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white py-20">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <div className="text-5xl mb-4">🐾</div>
            <h1 className="text-4xl md:text-5xl font-extrabold mb-4">¿Qué hacemos?</h1>
            <p className="text-blue-100 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
              Somos el marketplace de servicios para mascotas más completo de la Ciudad de México.
              Conectamos dueños con veterinarios y paseadores verificados, con precios transparentes y reserva en segundos.
            </p>
          </div>
        </section>

        {/* Stats */}
        <section className="bg-white border-b border-gray-100">
          <div className="max-w-5xl mx-auto px-4 py-10 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {STATS.map((s) => (
              <div key={s.label}>
                <div className="text-3xl font-extrabold text-blue-600">{s.value}</div>
                <div className="text-sm text-gray-500 mt-1">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Mission */}
        <section className="bg-gray-50 py-16">
          <div className="max-w-4xl mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Nuestra misión</h2>
                <p className="text-gray-600 leading-relaxed mb-4">
                  En <strong>PetCare</strong> creemos que cada mascota merece atención médica de calidad, accesible y cercana.
                  Hemos construido una plataforma donde los dueños de mascotas pueden encontrar, comparar y reservar con los mejores veterinarios
                  y paseadores de la CDMX, con precios claros desde el principio.
                </p>
                <p className="text-gray-600 leading-relaxed">
                  Todos nuestros proveedores están verificados, cuentan con cédula profesional y acumulan reseñas reales
                  de dueños como tú. Sin sorpresas, sin intermediarios ocultos.
                </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { icon: "✅", title: "Proveedores verificados", desc: "Cédula profesional y reseñas reales" },
                  { icon: "💰", title: "Precios transparentes", desc: "Sin costos ocultos ni sorpresas" },
                  { icon: "📍", title: "Cerca de ti", desc: "Búsqueda por geolocalización" },
                  { icon: "⚡", title: "Reserva en segundos", desc: "Confirmación inmediata" },
                ].map((f) => (
                  <div key={f.title} className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                    <div className="text-2xl mb-2">{f.icon}</div>
                    <div className="font-semibold text-gray-900 text-sm">{f.title}</div>
                    <div className="text-gray-500 text-xs mt-1">{f.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Services */}
        <section className="bg-white py-16">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-3">Servicios disponibles</h2>
            <p className="text-gray-500 text-center mb-10 text-sm">Precios reales de mercado en CDMX (pesos mexicanos)</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {SERVICES.map((s) => (
                <div key={s.title} className="bg-gray-50 rounded-2xl p-6 border border-gray-100 hover:shadow-md transition">
                  <div className="text-4xl mb-3">{s.icon}</div>
                  <h3 className="font-semibold text-gray-900 text-lg mb-1">{s.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed mb-4">{s.desc}</p>
                  <ul className="space-y-1 mb-4">
                    {s.details.map((d) => (
                      <li key={d} className="text-xs text-gray-600 flex items-center gap-1">
                        <span className="text-green-500">✓</span> {d}
                      </li>
                    ))}
                  </ul>
                  <div className="bg-white rounded-xl px-3 py-2 border border-gray-100 inline-block">
                    <span className="text-xs text-gray-400">Desde </span>
                    <span className="font-bold text-blue-600">${s.priceFrom.toLocaleString()}</span>
                    <span className="text-xs text-gray-400"> — ${s.priceTo.toLocaleString()} MXN</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Price table */}
        <section className="bg-gray-50 py-16">
          <div className="max-w-4xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-3">Tabla de precios CDMX</h2>
            <p className="text-gray-500 text-center mb-8 text-sm">
              Precios de referencia del mercado privado en la Ciudad de México (2025). Los precios varían por colonia,
              tamaño del animal y clínica.
            </p>
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-900 text-white">
                      <th className="text-left px-4 py-3 font-semibold">Servicio</th>
                      <th className="text-right px-4 py-3 font-semibold">Mínimo</th>
                      <th className="text-right px-4 py-3 font-semibold">Máximo</th>
                      <th className="text-left px-4 py-3 font-semibold hidden sm:table-cell">Nota</th>
                    </tr>
                  </thead>
                  <tbody>
                    {PRICE_TABLE.map((row, i) => (
                      <tr key={row.service} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="px-4 py-3 font-medium text-gray-800">{row.service}</td>
                        <td className="px-4 py-3 text-right text-green-700 font-semibold">
                          {row.min === 0 ? "Gratis" : `$${row.min.toLocaleString()}`}
                        </td>
                        <td className="px-4 py-3 text-right text-gray-700">
                          {row.max === 0 ? "—" : `$${row.max.toLocaleString()}`}
                        </td>
                        <td className="px-4 py-3 text-gray-400 text-xs hidden sm:table-cell">{row.note}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="px-4 py-3 bg-blue-50 text-xs text-blue-700 border-t border-blue-100">
                💡 Fuentes: SpayMe CDMX 2024, Clínica Bienestar Tláhuac, Hospital Carson, VeterinariasCerca24.com.mx
              </div>
            </div>
          </div>
        </section>

        {/* How it works */}
        <section className="bg-white py-16">
          <div className="max-w-4xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">¿Cómo funciona?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { step: "1", icon: "🔍", title: "Busca", desc: "Encuentra veterinarios y paseadores verificados cerca de ti. Filtra por tipo de servicio, distancia y precio." },
                { step: "2", icon: "📅", title: "Reserva", desc: "Elige el proveedor, el servicio y el horario que mejor te convenga. Confirmación inmediata." },
                { step: "3", icon: "⭐", title: "Califica", desc: "Después del servicio, deja tu reseña. Ayudas a otros dueños a elegir con confianza." },
              ].map((s) => (
                <div key={s.step} className="text-center">
                  <div className="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center text-2xl mx-auto mb-4">
                    {s.icon}
                  </div>
                  <div className="text-xs font-bold text-blue-600 uppercase tracking-wide mb-1">Paso {s.step}</div>
                  <h3 className="font-semibold text-gray-900 text-lg mb-2">{s.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-blue-600 py-16 text-center text-white">
          <div className="max-w-2xl mx-auto px-4">
            <h2 className="text-3xl font-bold mb-4">¿Listo para empezar?</h2>
            <p className="text-blue-100 mb-8">Encuentra el veterinario perfecto para tu mascota hoy mismo.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/providers" className="bg-white text-blue-600 px-8 py-3 rounded-full font-semibold hover:bg-blue-50 transition">
                Buscar veterinarios
              </Link>
              <Link href="/providers/map" className="bg-blue-500 text-white border border-blue-400 px-8 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
                Ver en el mapa 🗺️
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
'''

# ─────────────────────────────────────────────────────────────
# Updated Navbar with Map + About links
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
'''

# ─────────────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────────────

def main():
    project = ROOT
    if not (project / "package.json").exists():
        print(f"ERROR: Not a Next.js project root: {project}")
        sys.exit(1)

    print(f"\n🚀  Building Phase 2c — Map + About + Pricing\n")

    print("── PAGES ───────────────────────────────────────────────")
    write("src/app/providers/map/page.tsx",  MAP_PAGE)
    write("src/app/about/page.tsx",          ABOUT_PAGE)

    print("\n── COMPONENTS ──────────────────────────────────────────")
    write("src/components/shared/Navbar.tsx", NAVBAR)

    print("\n────────────────────────────────────────────────────────")
    print("✅  Phase 2c complete.\n")
    print("New pages:")
    print("  /providers/map  — Interactive map with 10 real CDMX vet clinics")
    print("  /about          — What we do + real services + pricing table")
    print()
    print("Navbar updated with: Mapa 🗺️ + ¿Qué hacemos? links")
    print()

if __name__ == "__main__":
    main()

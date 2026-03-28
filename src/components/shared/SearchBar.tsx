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
          placeholder="Buscar por nombre, servicio, raza…"
          className="w-full pl-9 pr-4 py-3 rounded-xl border border-gray-200 bg-white text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
        className="px-4 py-3 rounded-xl border border-gray-200 bg-white text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
      >
        <option value="">Todos los proveedores</option>
        <option value="VETERINARIAN">🏥 Veterinarios</option>
        <option value="PET_WALKER">🦮 Paseadores</option>
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
        Buscar
      </button>
    </form>
  );
}

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
  VETERINARIAN: "🏥 Veterinario",
  PET_WALKER:   "🦮 Paseador",
};

const TYPE_COLOR: Record<string, string> = {
  VETERINARIAN: "bg-green-100 text-green-700",
  PET_WALKER:   "bg-orange-100 text-orange-700",
};

function Stars({ rating, count }: { rating: number; count?: number }) {
  return (
    <div className="flex items-center gap-1 text-sm">
      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
      <span className="font-semibold text-gray-900">{rating.toFixed(1)}</span>
      {count !== undefined && <span className="text-gray-400">({count} reseñas)</span>}
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
            <span className="truncate">{city ?? "Ubicación no disponible"}</span>
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
          {services.length > 3 && <span className="text-xs text-gray-400 px-1 py-1">+{services.length - 3} más</span>}
        </div>
      )}

      <div className="mt-auto px-5 py-4 flex items-center justify-between border-t border-gray-50">
        {lowestPrice != null ? (
          <div className="flex items-center gap-1 text-sm text-gray-700">
            <DollarSign className="w-4 h-4 text-green-600" />
            <span>Desde <strong>${lowestPrice}</strong></span>
          </div>
        ) : (
          <span className="text-sm text-gray-400">Precio a consultar</span>
        )}
        <Link href={`/providers/${id}`} className="bg-blue-600 text-white text-sm font-semibold px-4 py-2 rounded-full hover:bg-blue-700 transition">
          Reservar
        </Link>
      </div>
    </div>
  );
}

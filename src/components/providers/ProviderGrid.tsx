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
        <h3 className="text-lg font-semibold text-gray-700 mb-1">No se encontraron proveedores</h3>
        <p className="text-sm">Intenta ajustar los filtros o ampliar el radio de búsqueda.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {providers.map((p) => <ProviderCard key={p.id} {...p} />)}
    </div>
  );
}

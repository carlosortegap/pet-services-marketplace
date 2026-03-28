import { useCallback, useState } from "react";
import type { SearchProvidersInput } from "@/lib/validations/provider";

export function useProviders() {
  const [providers, setProviders] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState<any>(null);

  const search = useCallback(async (params: Partial<SearchProvidersInput>) => {
    setLoading(true);
    try {
      const qs = new URLSearchParams(
        Object.entries(params)
          .filter(([, v]) => v != null)
          .map(([k, v]) => [k, String(v)])
      ).toString();

      const res = await fetch(`/api/providers?${qs}`);
      const data = await res.json();
      setProviders(data.providers);
      setPagination(data.pagination);
    } finally {
      setLoading(false);
    }
  }, []);

  return { providers, loading, pagination, search };
}

import { z } from "zod";
import { ProviderType } from "@prisma/client";

export const searchProvidersSchema = z.object({
  query:     z.string().min(1).max(100).optional().nullable(),
  type:      z.nativeEnum(ProviderType).optional().nullable(),
  lat:       z.coerce.number().min(-90).max(90).optional().nullable(),
  lng:       z.coerce.number().min(-180).max(180).optional().nullable(),
  radius:    z.coerce.number().min(1).max(100).catch(10).default(10),
  minRating: z.coerce.number().min(1).max(5).optional().nullable(),
  maxPrice:  z.coerce.number().min(0).optional().nullable(),
  sortBy:    z.enum(["rating", "distance", "reviews", "newest"]).catch("rating").default("rating"),
  page:      z.coerce.number().min(1).catch(1).default(1),
  limit:     z.coerce.number().min(1).max(50).catch(12).default(12),
});

export type SearchProvidersInput = z.infer<typeof searchProvidersSchema>;

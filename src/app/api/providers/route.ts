import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { rateLimit } from "@/lib/rate-limit";
import { searchProvidersSchema } from "@/lib/validations/provider";

const providerSelectFields = {
  specializations: true,
  images: { where: { isPrimary: true }, take: 1 },
  services: { where: { isActive: true }, orderBy: { price: "asc" as const }, take: 3 },
  user: { select: { id: true, name: true } },
};

type GeoProvider = { id: string; distance_km: number };

export async function GET(req: NextRequest) {
  try {
    const ip = req.headers.get("x-forwarded-for") ?? "unknown";
    const { success } = await rateLimit(ip);
    if (!success) return NextResponse.json({ error: "Too many requests" }, { status: 429 });

    const { searchParams } = new URL(req.url);

    const parsed = searchProvidersSchema.safeParse({
      query: searchParams.get("query"),
      type: searchParams.get("type"),
      lat: searchParams.get("lat"),
      lng: searchParams.get("lng"),
      radius: searchParams.get("radius"),
      minRating: searchParams.get("minRating"),
      maxPrice: searchParams.get("maxPrice"),
      sortBy: searchParams.get("sortBy"),
      page: searchParams.get("page"),
      limit: searchParams.get("limit"),
    });

    if (!parsed.success) {
      return NextResponse.json({ error: "Invalid search parameters", issues: parsed.error.flatten() }, { status: 422 });
    }

    const { query, type, lat, lng, radius = 10, minRating, maxPrice, sortBy = "rating", page = 1, limit = 12 } = parsed.data;
    const skip = (page - 1) * limit;

    // Standard search (no geo)
    if (!lat || !lng) {
      const where: any = {
        isAvailable: true,
        ...(type && { type }),
        ...(minRating && { rating: { gte: minRating } }),
        ...(query && {
          OR: [
            { displayName: { contains: query, mode: "insensitive" } },
            { clinicName: { contains: query, mode: "insensitive" } },
            { bio: { contains: query, mode: "insensitive" } },
            { city: { contains: query, mode: "insensitive" } },
            { specializations: { some: { name: { contains: query, mode: "insensitive" } } } },
            { services: { some: { name: { contains: query, mode: "insensitive" }, isActive: true } } },
          ],
        }),
        ...(maxPrice && { services: { some: { price: { lte: maxPrice }, isActive: true } } }),
      };

      const orderBy =
        sortBy === "rating" ? { rating: "desc" as const } :
        sortBy === "reviews" ? { reviewCount: "desc" as const } :
        sortBy === "newest" ? { createdAt: "desc" as const } :
        { rating: "desc" as const };

      const [providers, total] = await Promise.all([
        prisma.providerProfile.findMany({ where, skip, take: limit, orderBy, include: providerSelectFields }),
        prisma.providerProfile.count({ where }),
      ]);

      return NextResponse.json({
        providers,
        pagination: { page, limit, total, pages: Math.ceil(total / limit) },
        searchType: "standard",
      });
    }

    // Geo search (Haversine)
    const geoResults = await prisma.$queryRaw<GeoProvider[]>`
      SELECT
        p.id,
        (6371 * acos(
          cos(radians(${lat})) * cos(radians(p.latitude)) *
          cos(radians(p.longitude) - radians(${lng})) +
          sin(radians(${lat})) * sin(radians(p.latitude))
        )) AS distance_km
      FROM "ProviderProfile" p
      WHERE
        p."isAvailable" = true
        AND (${type}::text IS NULL OR p.type::text = ${type}::text)
        AND (${minRating ?? null}::float IS NULL OR p.rating >= ${minRating ?? 0})
        AND (6371 * acos(
          cos(radians(${lat})) * cos(radians(p.latitude)) *
          cos(radians(p.longitude) - radians(${lng})) +
          sin(radians(${lat})) * sin(radians(p.latitude))
        )) <= ${radius}
      ORDER BY ${sortBy === "distance" ? "distance_km ASC" : "p.rating DESC"}
      LIMIT ${limit} OFFSET ${skip}
    `;

    const providerIds = geoResults.map((p) => p.id);
    const enriched = await prisma.providerProfile.findMany({
      where: { id: { in: providerIds } },
      include: providerSelectFields,
    });

    const withDistance = providerIds.map((id) => {
      const provider = enriched.find((p) => p.id === id)!;
      const geo = geoResults.find((p) => p.id === id)!;
      return { ...provider, distanceKm: Math.round(geo.distance_km * 10) / 10 };
    });

    const totalGeo = await prisma.$queryRaw<[{ count: bigint }]>`
      SELECT COUNT(*) as count FROM "ProviderProfile" p
      WHERE p."isAvailable" = true
      AND (${type}::text IS NULL OR p.type::text = ${type}::text)
      AND (6371 * acos(
        cos(radians(${lat})) * cos(radians(p.latitude)) *
        cos(radians(p.longitude) - radians(${lng})) +
        sin(radians(${lat})) * sin(radians(p.latitude))
      )) <= ${radius}
    `;

    return NextResponse.json({
      providers: withDistance,
      pagination: { page, limit, total: Number(totalGeo[0].count), pages: Math.ceil(Number(totalGeo[0].count) / limit) },
      searchType: "geo",
      center: { lat, lng },
      radiusKm: radius,
    });
  } catch (error) {
    console.error("[GET /api/providers]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

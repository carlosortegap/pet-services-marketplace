import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

type Params = { params: Promise<{ id: string }> };

export async function GET(_req: NextRequest, { params }: Params) {
  try {
    const { id } = await params;
    const provider = await prisma.providerProfile.findUnique({
      where: { id, isAvailable: true },
      include: {
        specializations: true,
        services: { where: { isActive: true }, orderBy: { price: "asc" } },
        availability: { where: { isActive: true }, orderBy: { dayOfWeek: "asc" } },
        images: { orderBy: { isPrimary: "desc" } },
        reviewsReceived: {
          where: { isPublished: true }, orderBy: { createdAt: "desc" }, take: 10,
          include: { author: { select: { id: true, name: true, avatarUrl: true } } },
        },
        user: { select: { id: true, name: true, createdAt: true } },
        _count: { select: { reviewsReceived: true, bookings: true } },
      },
    });
    if (!provider) return NextResponse.json({ error: "Provider not found" }, { status: 404 });
    return NextResponse.json({ provider });
  } catch (error) {
    console.error("[GET /api/providers/[id]]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

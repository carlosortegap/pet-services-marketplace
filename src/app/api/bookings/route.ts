import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { createBookingSchema } from "@/lib/validations/booking";
import { BookingStatus, PaymentStatus, SubscriptionTier } from "@prisma/client";
import { rateLimit } from "@/lib/rate-limit";

// GET /api/bookings
export async function GET(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const status = searchParams.get("status") as BookingStatus | null;
    const page = parseInt(searchParams.get("page") ?? "1");
    const limit = Math.min(parseInt(searchParams.get("limit") ?? "10"), 50);
    const skip = (page - 1) * limit;

    const where =
      session.user.role === "PROVIDER"
        ? { providerProfile: { userId: session.user.id }, ...(status && { status }) }
        : { ownerId: session.user.id, ...(status && { status }) };

    const [bookings, total] = await Promise.all([
      prisma.booking.findMany({
        where,
        skip,
        take: limit,
        orderBy: { scheduledAt: "desc" },
        include: {
          service: true,
          pet: true,
          providerProfile: {
            select: { id: true, displayName: true, avatarUrl: true, type: true, city: true },
          },
          owner: { select: { id: true, name: true, avatarUrl: true } },
          review: { select: { id: true, rating: true } },
        },
      }),
      prisma.booking.count({ where }),
    ]);

    return NextResponse.json({
      bookings,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    });
  } catch (error) {
    console.error("[GET /api/bookings]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

// POST /api/bookings
export async function POST(req: NextRequest) {
  try {
    const ip = req.headers.get("x-forwarded-for") ?? "unknown";
    const { success } = await rateLimit(ip);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const body = await req.json();
    const parsed = createBookingSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: "Validation failed", issues: parsed.error.flatten() }, { status: 422 });
    }

    const { providerProfileId, serviceId, petId, scheduledAt, notes } = parsed.data;

    // FREE tier limit check
    const user = await prisma.user.findUnique({
      where: { id: session.user.id },
      select: { subscriptionTier: true },
    });

    if (user?.subscriptionTier === SubscriptionTier.FREE) {
      const startOfMonth = new Date();
      startOfMonth.setDate(1);
      startOfMonth.setHours(0, 0, 0, 0);

      const monthlyCount = await prisma.booking.count({
        where: {
          ownerId: session.user.id,
          createdAt: { gte: startOfMonth },
          status: { not: BookingStatus.CANCELLED },
        },
      });

      if (monthlyCount >= 5) {
        return NextResponse.json(
          { error: "Monthly booking limit reached", upgrade: true, message: "Upgrade to Professional for unlimited bookings" },
          { status: 403 }
        );
      }
    }

    const [service, providerProfile, pet] = await Promise.all([
      prisma.service.findUnique({ where: { id: serviceId, providerProfileId, isActive: true } }),
      prisma.providerProfile.findUnique({ where: { id: providerProfileId, isAvailable: true }, select: { id: true, userId: true, isAvailable: true } }),
      prisma.pet.findUnique({ where: { id: petId }, select: { id: true, ownerProfile: { select: { userId: true } } } }),
    ]);

    if (!service) return NextResponse.json({ error: "Service not found or inactive" }, { status: 404 });
    if (!providerProfile) return NextResponse.json({ error: "Provider not found or unavailable" }, { status: 404 });
    if (!pet || pet.ownerProfile.userId !== session.user.id) return NextResponse.json({ error: "Pet not found or not yours" }, { status: 404 });
    if (providerProfile.userId === session.user.id) return NextResponse.json({ error: "Cannot book your own service" }, { status: 400 });

    // Conflict check
    const scheduledDate = new Date(scheduledAt);
    const endTime = new Date(scheduledDate.getTime() + service.durationMinutes * 60000);
    const conflict = await prisma.booking.findFirst({
      where: {
        providerProfileId,
        status: { in: [BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS] },
        AND: [
          { scheduledAt: { lt: endTime } },
          { scheduledAt: { gt: new Date(scheduledDate.getTime() - service.durationMinutes * 60000) } },
        ],
      },
    });

    if (conflict) return NextResponse.json({ error: "Provider is not available at this time" }, { status: 409 });

    const PLATFORM_FEE_RATE = 0.15;
    const platformFee = Math.round(service.price * PLATFORM_FEE_RATE * 100) / 100;
    const providerPayout = Math.round((service.price - platformFee) * 100) / 100;

    const booking = await prisma.booking.create({
      data: {
        ownerId: session.user.id,
        providerProfileId,
        serviceId,
        petId,
        scheduledAt: scheduledDate,
        durationMinutes: service.durationMinutes,
        totalAmount: service.price,
        platformFee,
        providerPayout,
        notes,
        status: BookingStatus.PENDING,
        paymentStatus: PaymentStatus.PENDING,
      },
      include: { service: true, pet: true, providerProfile: { select: { id: true, displayName: true, type: true } } },
    });

    return NextResponse.json({ booking }, { status: 201 });
  } catch (error) {
    console.error("[POST /api/bookings]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

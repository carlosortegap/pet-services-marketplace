import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { updateBookingSchema } from "@/lib/validations/booking";
import { BookingStatus } from "@prisma/client";

type Params = { params: Promise<{ id: string }> };

export async function GET(_req: NextRequest, { params }: Params) {
  try {
    const { id } = await params;
    const session = await getServerSession(authOptions);
    if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    const booking = await prisma.booking.findUnique({
      where: { id },
      include: {
        service: true, pet: true,
        providerProfile: { include: { specializations: true, images: { where: { isPrimary: true }, take: 1 } } },
        owner: { select: { id: true, name: true, email: true, avatarUrl: true } },
        review: true, transaction: true,
      },
    });

    if (!booking) return NextResponse.json({ error: "Booking not found" }, { status: 404 });
    const isOwner = booking.ownerId === session.user.id;
    const isProvider = booking.providerProfile.userId === session.user.id;
    if (!isOwner && !isProvider && session.user.role !== "ADMIN") return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    return NextResponse.json({ booking });
  } catch (error) {
    console.error("[GET /api/bookings/[id]]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

export async function PATCH(req: NextRequest, { params }: Params) {
  try {
    const { id } = await params;
    const session = await getServerSession(authOptions);
    if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    const parsed = updateBookingSchema.safeParse(await req.json());
    if (!parsed.success) return NextResponse.json({ error: "Validation failed", issues: parsed.error.flatten() }, { status: 422 });

    const booking = await prisma.booking.findUnique({
      where: { id },
      include: { providerProfile: { select: { userId: true } } },
    });
    if (!booking) return NextResponse.json({ error: "Booking not found" }, { status: 404 });

    const isOwner = booking.ownerId === session.user.id;
    const isProvider = booking.providerProfile.userId === session.user.id;
    const allowed: Record<string, BookingStatus[]> = {
      PROVIDER: [BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS, BookingStatus.COMPLETED],
      OWNER: [BookingStatus.CANCELLED], ADMIN: Object.values(BookingStatus),
    };
    const role = session.user.role === "ADMIN" ? "ADMIN" : isProvider ? "PROVIDER" : "OWNER";
    if (!isOwner && !isProvider && role !== "ADMIN") return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    if (!allowed[role].includes(parsed.data.status)) return NextResponse.json({ error: `${role} cannot set status to ${parsed.data.status}` }, { status: 403 });

    const updated = await prisma.booking.update({
      where: { id },
      data: { status: parsed.data.status, ...(parsed.data.status === BookingStatus.CANCELLED && { cancelledAt: new Date(), cancelReason: parsed.data.cancelReason }) },
      include: { service: true, pet: true },
    });
    return NextResponse.json({ booking: updated });
  } catch (error) {
    console.error("[PATCH /api/bookings/[id]]", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

export async function DELETE(req: NextRequest, { params }: Params) {
  const { id } = await params;
  return PATCH(new NextRequest(req.url, { method: "PATCH", body: JSON.stringify({ status: "CANCELLED" }) }), { params: Promise.resolve({ id }) });
}

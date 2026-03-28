import { prisma } from "@/lib/prisma";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { notFound, redirect } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";
import { Calendar, Clock, DollarSign, MapPin } from "lucide-react";

interface Props { params: { id: string } }

const STATUS_COLOR: Record<string, string> = {
  PENDING: "bg-yellow-100 text-yellow-700",
  CONFIRMED: "bg-blue-100 text-blue-700",
  IN_PROGRESS: "bg-purple-100 text-purple-700",
  COMPLETED: "bg-green-100 text-green-700",
  CANCELLED: "bg-red-100 text-red-700",
  DISPUTED: "bg-orange-100 text-orange-700",
};

export default async function BookingDetailPage({ params }: Props) {
  const session = await getServerSession(authOptions);
  if (!session) redirect("/login");

  const booking = await prisma.booking.findUnique({
    where: { id: params.id },
    include: {
      owner: { select: { name: true, email: true } },
      providerProfile: { select: { displayName: true, city: true, type: true } },
      service: true,
      pet: true,
    },
  });

  if (!booking) notFound();

  // Only owner or the provider can view
  const isOwner = booking.ownerId === session.user.id;
  const providerUser = await prisma.providerProfile.findUnique({
    where: { id: booking.providerProfileId },
    select: { userId: true },
  });
  const isProvider = providerUser?.userId === session.user.id;
  if (!isOwner && !isProvider) redirect("/");

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
            {/* Header */}
            <div className="bg-blue-600 px-6 py-6 text-white">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-blue-200 text-xs mb-1">Booking #{booking.id.slice(-8).toUpperCase()}</p>
                  <h1 className="text-xl font-bold">{booking.service.name}</h1>
                  <p className="text-blue-100 text-sm mt-1">{booking.providerProfile.displayName}</p>
                </div>
                <span className={`text-xs font-semibold px-3 py-1 rounded-full ${STATUS_COLOR[booking.status] ?? "bg-gray-100 text-gray-600"}`}>
                  {booking.status}
                </span>
              </div>
            </div>

            {/* Details */}
            <div className="p-6 space-y-5">
              <Row icon={Calendar} label="Date & Time" value={new Date(booking.scheduledAt).toLocaleString("en-MX", { dateStyle: "full", timeStyle: "short" })} />
              <Row icon={Clock} label="Duration" value={`${booking.durationMinutes} minutes`} />
              <Row icon={MapPin} label="Location" value={booking.providerProfile.city} />
              <Row icon={DollarSign} label="Total" value={`$${booking.totalAmount.toLocaleString()} MXN`} />

              <hr className="border-gray-100" />

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-gray-50 rounded-xl p-4">
                  <p className="text-xs text-gray-400 mb-1">Pet</p>
                  <p className="font-semibold text-gray-800">{booking.pet.name}</p>
                  <p className="text-xs text-gray-500">{booking.pet.breed ?? booking.pet.species}</p>
                </div>
                <div className="bg-gray-50 rounded-xl p-4">
                  <p className="text-xs text-gray-400 mb-1">Owner</p>
                  <p className="font-semibold text-gray-800">{booking.owner.name}</p>
                  <p className="text-xs text-gray-500">{booking.owner.email}</p>
                </div>
              </div>

              {booking.notes && (
                <div className="bg-blue-50 rounded-xl p-4 text-sm text-blue-800">
                  <p className="text-xs text-blue-400 mb-1">Notes</p>
                  {booking.notes}
                </div>
              )}
            </div>

            <div className="px-6 pb-6">
              <Link
                href={isOwner ? "/dashboard/owner" : "/dashboard/provider"}
                className="block w-full text-center bg-gray-900 text-white py-3 rounded-xl font-semibold text-sm hover:bg-gray-700 transition"
              >
                ← Back to dashboard
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

function Row({ icon: Icon, label, value }: { icon: React.ElementType; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
        <Icon className="w-4 h-4 text-gray-500" />
      </div>
      <div>
        <p className="text-xs text-gray-400">{label}</p>
        <p className="font-medium text-gray-800">{value}</p>
      </div>
    </div>
  );
}

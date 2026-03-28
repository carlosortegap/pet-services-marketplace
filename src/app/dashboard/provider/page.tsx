import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Calendar, Star, DollarSign, Users } from "lucide-react";

export default async function ProviderDashboard() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) return null;

  const profile = await prisma.providerProfile.findUnique({
    where: { userId: session.user.id },
    include: { services: true },
  });

  const bookings = await prisma.booking.findMany({
    where: { providerProfileId: profile?.id },
    include: {
      owner: { select: { name: true } },
      service: { select: { name: true } },
      pet: { select: { name: true, species: true } },
    },
    orderBy: { scheduledAt: "desc" },
    take: 6,
  });

  const totalRevenue = bookings
    .filter((b) => b.status === "COMPLETED")
    .reduce((sum, b) => sum + b.providerPayout, 0);

  const STATUS_COLOR: Record<string, string> = {
    PENDING: "bg-yellow-100 text-yellow-700",
    CONFIRMED: "bg-blue-100 text-blue-700",
    IN_PROGRESS: "bg-purple-100 text-purple-700",
    COMPLETED: "bg-green-100 text-green-700",
    CANCELLED: "bg-red-100 text-red-700",
    DISPUTED: "bg-orange-100 text-orange-700",
  };

  const stats = [
    { icon: Calendar, label: "Total Bookings", value: profile?.bookingCount ?? 0, color: "text-blue-600" },
    { icon: Star, label: "Avg Rating", value: profile ? profile.rating.toFixed(1) + " ⭐" : "—", color: "text-yellow-500" },
    { icon: Users, label: "Reviews", value: profile?.reviewCount ?? 0, color: "text-indigo-600" },
    { icon: DollarSign, label: "Total Earned", value: `$${totalRevenue.toLocaleString()}`, color: "text-green-600" },
  ];

  if (!profile) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center">
        <div className="text-5xl mb-4">🏗️</div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Complete your profile</h1>
        <p className="text-gray-500 mb-6">Set up your provider profile to start accepting bookings.</p>
        <Link href="/profile/setup" className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
          Set up profile
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {profile.displayName}
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            {profile.type === "VETERINARIAN" ? "🏥 Veterinarian" : "🦮 Pet Walker"} · {profile.city}
          </p>
        </div>
        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${profile.isAvailable ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
          {profile.isAvailable ? "● Available" : "○ Unavailable"}
        </span>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-2xl border border-gray-100 p-5 text-center">
            <s.icon className={`w-5 h-5 mx-auto mb-2 ${s.color}`} />
            <div className="text-xl font-bold text-gray-900">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Services */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">My Services</h2>
          {profile.services.length ? (
            <div className="space-y-3">
              {profile.services.map((s) => (
                <div key={s.id} className="bg-white rounded-xl border border-gray-100 p-4 flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{s.name}</p>
                    <p className="text-xs text-gray-500">{s.durationMinutes} min</p>
                  </div>
                  <span className="font-bold text-green-700 text-sm">${s.price}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-gray-400 text-sm">
              No services added yet
            </div>
          )}
        </section>

        {/* Recent bookings */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Bookings</h2>
          {bookings.length ? (
            <div className="space-y-3">
              {bookings.map((b) => (
                <Link
                  key={b.id}
                  href={`/bookings/${b.id}`}
                  className="bg-white rounded-xl border border-gray-100 p-4 flex items-start justify-between hover:shadow-sm transition block"
                >
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{b.owner.name}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{b.service.name} · {b.pet.name}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {new Date(b.scheduledAt).toLocaleDateString("en-MX", { day: "numeric", month: "short" })}
                    </p>
                  </div>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[b.status] ?? "bg-gray-100 text-gray-600"}`}>
                    {b.status}
                  </span>
                </Link>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-sm text-gray-400">
              No bookings yet
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

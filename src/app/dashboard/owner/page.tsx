import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Calendar, PawPrint, Star, Search } from "lucide-react";

export default async function OwnerDashboard() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) return null;

  const owner = await prisma.ownerProfile.findUnique({
    where: { userId: session.user.id },
    include: {
      pets: true,
    },
  });

  const bookings = await prisma.booking.findMany({
    where: { ownerId: session.user.id },
    include: {
      providerProfile: { select: { displayName: true, city: true, type: true } },
      service: { select: { name: true } },
      pet: { select: { name: true } },
    },
    orderBy: { scheduledAt: "desc" },
    take: 5,
  });

  const STATUS_COLOR: Record<string, string> = {
    PENDING: "bg-yellow-100 text-yellow-700",
    CONFIRMED: "bg-blue-100 text-blue-700",
    IN_PROGRESS: "bg-purple-100 text-purple-700",
    COMPLETED: "bg-green-100 text-green-700",
    CANCELLED: "bg-red-100 text-red-700",
    DISPUTED: "bg-orange-100 text-orange-700",
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {session.user.name?.split(" ")[0]} 👋
        </h1>
        <p className="text-gray-500 text-sm mt-1">Manage your pets and bookings</p>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        {[
          { icon: Search, label: "Find a Provider", href: "/providers", color: "bg-blue-600" },
          { icon: Calendar, label: "My Bookings", href: "#bookings", color: "bg-indigo-600" },
          { icon: PawPrint, label: "My Pets", href: "#pets", color: "bg-green-600" },
        ].map((a) => (
          <Link
            key={a.label}
            href={a.href}
            className={`${a.color} text-white rounded-2xl p-5 flex items-center gap-3 hover:opacity-90 transition`}
          >
            <a.icon className="w-5 h-5" />
            <span className="font-semibold text-sm">{a.label}</span>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Pets */}
        <section id="pets">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <PawPrint className="w-5 h-5 text-green-600" /> My Pets
          </h2>
          {owner?.pets.length ? (
            <div className="space-y-3">
              {owner.pets.map((pet) => (
                <div key={pet.id} className="bg-white rounded-xl border border-gray-100 p-4 flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-xl">
                    {pet.species === "dog" ? "🐕" : pet.species === "cat" ? "🐈" : "🐾"}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">{pet.name}</p>
                    <p className="text-xs text-gray-500">{pet.breed ?? pet.species}{pet.age ? ` · ${pet.age}y` : ""}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-8 text-center text-gray-400 text-sm">
              No pets added yet
            </div>
          )}
        </section>

        {/* Recent Bookings */}
        <section id="bookings">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-blue-600" /> Recent Bookings
          </h2>
          {bookings.length ? (
            <div className="space-y-3">
              {bookings.map((b) => (
                <Link
                  key={b.id}
                  href={`/bookings/${b.id}`}
                  className="bg-white rounded-xl border border-gray-100 p-4 flex items-start justify-between hover:shadow-sm transition block"
                >
                  <div>
                    <p className="font-semibold text-gray-800 text-sm">{b.providerProfile.displayName}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{b.service.name} · {b.pet.name}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {new Date(b.scheduledAt).toLocaleDateString("en-MX", { day: "numeric", month: "short", year: "numeric" })}
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
              No bookings yet.{" "}
              <Link href="/providers" className="text-blue-600 hover:underline">Find a provider →</Link>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

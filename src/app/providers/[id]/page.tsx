import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import { Star, MapPin, Clock, DollarSign, CheckCircle } from "lucide-react";
import Link from "next/link";

interface Props { params: { id: string } }

export default async function ProviderDetailPage({ params }: Props) {
  const profile = await prisma.providerProfile.findUnique({
    where: { id: params.id },
    include: {
      user: { select: { name: true, email: true } },
      services: { where: { isActive: true } },
      specializations: true,
      reviewsReceived: {
        where: { isPublished: true },
        include: { author: { select: { name: true, avatarUrl: true } } },
        orderBy: { createdAt: "desc" },
        take: 5,
      },
    },
  });

  if (!profile) notFound();

  const typeLabel = profile.type === "VETERINARIAN" ? "🏥 Veterinarian" : "🦮 Pet Walker";

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        {/* Hero */}
        <div className="bg-white border-b border-gray-100">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="flex flex-col sm:flex-row items-start gap-6">
              <div className="w-24 h-24 rounded-2xl bg-blue-100 flex items-center justify-center text-4xl font-bold text-blue-600 flex-shrink-0">
                {profile.user.name?.[0]?.toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2 mb-1">
                  <h1 className="text-2xl font-bold text-gray-900">{profile.displayName}</h1>
                  {profile.isVerified && (
                    <span className="flex items-center gap-1 text-xs text-green-700 bg-green-100 px-2 py-0.5 rounded-full font-medium">
                      <CheckCircle className="w-3 h-3" /> Verified
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-500 mb-2">{typeLabel}</p>
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  {profile.rating > 0 && (
                    <span className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <strong>{profile.rating.toFixed(1)}</strong>
                      <span className="text-gray-400">({profile.reviewCount} reviews)</span>
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    {profile.city}
                  </span>
                  {profile.hourlyRate && (
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-4 h-4 text-green-600" />
                      From ${profile.hourlyRate}/hr
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Bio */}
            {profile.bio && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-3">About</h2>
                <p className="text-gray-600 text-sm leading-relaxed">{profile.bio}</p>
              </section>
            )}

            {/* Specializations */}
            {profile.specializations.length > 0 && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-3">Specializations</h2>
                <div className="flex flex-wrap gap-2">
                  {profile.specializations.map((s) => (
                    <span key={s.id} className="bg-blue-50 text-blue-700 text-xs font-medium px-3 py-1 rounded-full">
                      {s.name}
                    </span>
                  ))}
                </div>
              </section>
            )}

            {/* Reviews */}
            {profile.reviewsReceived.length > 0 && (
              <section className="bg-white rounded-2xl border border-gray-100 p-6">
                <h2 className="font-semibold text-gray-900 mb-4">Reviews</h2>
                <div className="space-y-4">
                  {profile.reviewsReceived.map((r) => (
                    <div key={r.id} className="border-b border-gray-50 last:border-0 pb-4 last:pb-0">
                      <div className="flex items-center gap-2 mb-1">
                        <div className="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-600">
                          {r.author.name?.[0]?.toUpperCase()}
                        </div>
                        <span className="text-sm font-medium text-gray-800">{r.author.name}</span>
                        <div className="flex ml-auto">
                          {Array.from({ length: r.rating }).map((_, i) => (
                            <Star key={i} className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                          ))}
                        </div>
                      </div>
                      {r.comment && <p className="text-sm text-gray-600 ml-9">{r.comment}</p>}
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>

          {/* Right column — services + booking CTA */}
          <div className="space-y-4">
            <div className="bg-white rounded-2xl border border-gray-100 p-6 sticky top-20">
              <h2 className="font-semibold text-gray-900 mb-4">Services</h2>
              {profile.services.length ? (
                <div className="space-y-3 mb-6">
                  {profile.services.map((s) => (
                    <div key={s.id} className="flex items-start justify-between gap-2">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{s.name}</p>
                        <p className="text-xs text-gray-400 flex items-center gap-1">
                          <Clock className="w-3 h-3" /> {s.durationMinutes} min
                        </p>
                      </div>
                      <span className="text-sm font-bold text-green-700 whitespace-nowrap">${s.price}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-400 mb-6">No services listed.</p>
              )}
              <Link
                href={`/login?callbackUrl=/providers/${profile.id}`}
                className="w-full bg-blue-600 text-white text-sm font-semibold py-3 rounded-xl hover:bg-blue-700 transition text-center block"
              >
                Book appointment
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

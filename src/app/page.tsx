import Hero from "@/components/providers/Hero";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen flex flex-col">
        <Hero />

        {/* Servicios */}
        <section className="bg-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Todo lo que tu mascota necesita
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { icon: "🏥", title: "Veterinarios", desc: "Vets certificados para consultas, vacunas y urgencias.", href: "/providers?type=VETERINARIAN" },
                { icon: "🦮", title: "Paseadores", desc: "Paseos diarios, grupales y estancias nocturnas de confianza.", href: "/providers?type=PET_WALKER" },
                { icon: "⭐", title: "Reseñas verificadas", desc: "Opiniones reales de dueños de mascotas. Reserva con confianza.", href: "/providers" },
              ].map((f) => (
                <Link
                  key={f.title}
                  href={f.href}
                  className="bg-gray-50 rounded-2xl p-8 text-center hover:shadow-md hover:-translate-y-1 transition-all duration-200 border border-gray-100 group"
                >
                  <div className="text-5xl mb-4">{f.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition">{f.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{f.desc}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Estadísticas */}
        <section className="bg-blue-600 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-white text-center">
              {[
                { value: "2,000+", label: "Dueños de mascotas" },
                { value: "250+",   label: "Proveedores" },
                { value: "4.8⭐",  label: "Calificación promedio" },
                { value: "10K+",   label: "Reservas realizadas" },
              ].map((s) => (
                <div key={s.label}>
                  <div className="text-4xl font-extrabold">{s.value}</div>
                  <div className="text-blue-200 mt-1 text-sm">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA proveedores */}
        <section className="bg-white py-20 text-center">
          <div className="max-w-2xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">¿Eres profesional del cuidado de mascotas?</h2>
            <p className="text-gray-600 mb-8">Únete a nuestro marketplace, define tus tarifas y conecta con miles de dueños de mascotas en tu zona.</p>
            <Link href="/register?role=provider" className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-700 transition inline-block">
              Únete como proveedor
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

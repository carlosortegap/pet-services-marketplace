import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import Link from "next/link";

const SERVICES = [
  {
    icon: "🩺",
    title: "Consulta General",
    desc: "Evaluación completa de salud, diagnóstico y plan de tratamiento con veterinarios certificados.",
    priceFrom: 300,
    priceTo: 600,
    details: ["Historia clínica completa", "Examen físico general", "Diagnóstico y receta", "Seguimiento post-consulta"],
  },
  {
    icon: "💉",
    title: "Vacunación",
    desc: "Esquemas de vacunación completos para perros y gatos, incluyendo core y no-core vaccines.",
    priceFrom: 250,
    priceTo: 600,
    details: ["Vacuna antirrábica", "Quíntuple / Séxtuple", "Triple felina", "Bordetella y Giardia"],
  },
  {
    icon: "🦷",
    title: "Limpieza Dental",
    desc: "Profilaxis dental profesional con ultrasonido y pulido bajo sedación inhalada.",
    priceFrom: 1400,
    priceTo: 2200,
    details: ["Ultrasonido escariador", "Pulido dental", "Anestesia inhalada", "Evaluación periodontal"],
  },
  {
    icon: "✂️",
    title: "Castración y Esterilización",
    desc: "Procedimiento quirúrgico seguro para controlar la reproducción y mejorar la calidad de vida.",
    priceFrom: 700,
    priceTo: 2800,
    details: ["Preanestesia y monitoreo", "Cirugía laparoscópica disponible", "Recuperación en clínica", "Cuidados post-operatorios"],
  },
  {
    icon: "📷",
    title: "Estudios de Imagen",
    desc: "Radiografías y ultrasonido para diagnóstico preciso de órganos internos.",
    priceFrom: 400,
    priceTo: 1800,
    details: ["Ultrasonido abdominal", "Rayos X (1-2 placas)", "Ecocardiograma", "Resultado en el día"],
  },
  {
    icon: "🔬",
    title: "Laboratorio Clínico",
    desc: "Análisis de sangre, orina y biopsias para diagnóstico completo.",
    priceFrom: 600,
    priceTo: 2000,
    details: ["Biometría hemática", "Química sanguínea", "Urianálisis", "Pruebas de enfermedades infecciosas"],
  },
  {
    icon: "🚨",
    title: "Urgencias 24 horas",
    desc: "Atención de emergencias veterinarias las 24 horas del día, los 7 días de la semana.",
    priceFrom: 500,
    priceTo: 1800,
    details: ["Atención inmediata", "UCI veterinaria", "Oxigenoterapia", "Cirugía de emergencia"],
  },
  {
    icon: "🏥",
    title: "Hospitalización",
    desc: "Internamiento con monitoreo constante, medicación y cuidados de enfermería.",
    priceFrom: 500,
    priceTo: 1500,
    details: ["Monitoreo 24h", "Medicación IV", "Alimentación especializada", "Reportes diarios"],
  },
  {
    icon: "🦮",
    title: "Paseos y Cuidado",
    desc: "Paseadores certificados con rastreo GPS, seguro incluido y reportes por foto.",
    priceFrom: 120,
    priceTo: 350,
    details: ["GPS en tiempo real", "Fotos y reporte", "Máximo 4 perros por grupo", "Seguro de responsabilidad"],
  },
];

const PRICE_TABLE = [
  { service: "Consulta general", min: 300, max: 600, note: "Privada" },
  { service: "Consulta urgencias", min: 500, max: 1800, note: "Según horario" },
  { service: "Vacunación completa", min: 250, max: 600, note: "Perro o gato" },
  { service: "Antirrábica", min: 0, max: 300, note: "Gratis en módulos CDMX" },
  { service: "Limpieza dental (gato/peq)", min: 1400, max: 1800, note: "Con anestesia" },
  { service: "Limpieza dental (grande)", min: 1800, max: 2600, note: "Con anestesia" },
  { service: "Castración macho", min: 700, max: 1800, note: "Según tamaño" },
  { service: "Esterilización hembra", min: 800, max: 2800, note: "Según tamaño" },
  { service: "Ultrasonido abdominal", min: 400, max: 1800, note: "" },
  { service: "Radiografía (placa)", min: 500, max: 1500, note: "" },
  { service: "Panel de sangre completo", min: 600, max: 2000, note: "" },
  { service: "Hospitalización (por noche)", min: 500, max: 1500, note: "" },
  { service: "Desparasitación", min: 200, max: 500, note: "" },
  { service: "Microchip", min: 900, max: 900, note: "Precio fijo aprox." },
  { service: "Paseo solo 30 min", min: 120, max: 200, note: "Con GPS" },
  { service: "Paseo solo 60 min", min: 200, max: 350, note: "Con GPS" },
  { service: "Entrenamiento básico", min: 300, max: 500, note: "Por sesión" },
];

const STATS = [
  { value: "10+", label: "Clínicas verificadas" },
  { value: "250+", label: "Proveedores en CDMX" },
  { value: "4.8⭐", label: "Calificación promedio" },
  { value: "0%", label: "Comisión para reservar" },
];

export default function AboutPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen">
        {/* Hero */}
        <section className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white py-20">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <div className="text-5xl mb-4">🐾</div>
            <h1 className="text-4xl md:text-5xl font-extrabold mb-4">¿Qué hacemos?</h1>
            <p className="text-blue-100 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
              Somos el marketplace de servicios para mascotas más completo de la Ciudad de México.
              Conectamos dueños con veterinarios y paseadores verificados, con precios transparentes y reserva en segundos.
            </p>
          </div>
        </section>

        {/* Stats */}
        <section className="bg-white border-b border-gray-100">
          <div className="max-w-5xl mx-auto px-4 py-10 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {STATS.map((s) => (
              <div key={s.label}>
                <div className="text-3xl font-extrabold text-blue-600">{s.value}</div>
                <div className="text-sm text-gray-500 mt-1">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Mission */}
        <section className="bg-gray-50 py-16">
          <div className="max-w-4xl mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Nuestra misión</h2>
                <p className="text-gray-600 leading-relaxed mb-4">
                  En <strong>PetCare</strong> creemos que cada mascota merece atención médica de calidad, accesible y cercana.
                  Hemos construido una plataforma donde los dueños de mascotas pueden encontrar, comparar y reservar con los mejores veterinarios
                  y paseadores de la CDMX, con precios claros desde el principio.
                </p>
                <p className="text-gray-600 leading-relaxed">
                  Todos nuestros proveedores están verificados, cuentan con cédula profesional y acumulan reseñas reales
                  de dueños como tú. Sin sorpresas, sin intermediarios ocultos.
                </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { icon: "✅", title: "Proveedores verificados", desc: "Cédula profesional y reseñas reales" },
                  { icon: "💰", title: "Precios transparentes", desc: "Sin costos ocultos ni sorpresas" },
                  { icon: "📍", title: "Cerca de ti", desc: "Búsqueda por geolocalización" },
                  { icon: "⚡", title: "Reserva en segundos", desc: "Confirmación inmediata" },
                ].map((f) => (
                  <div key={f.title} className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                    <div className="text-2xl mb-2">{f.icon}</div>
                    <div className="font-semibold text-gray-900 text-sm">{f.title}</div>
                    <div className="text-gray-500 text-xs mt-1">{f.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Services */}
        <section className="bg-white py-16">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-3">Servicios disponibles</h2>
            <p className="text-gray-500 text-center mb-10 text-sm">Precios reales de mercado en CDMX (pesos mexicanos)</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {SERVICES.map((s) => (
                <div key={s.title} className="bg-gray-50 rounded-2xl p-6 border border-gray-100 hover:shadow-md transition">
                  <div className="text-4xl mb-3">{s.icon}</div>
                  <h3 className="font-semibold text-gray-900 text-lg mb-1">{s.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed mb-4">{s.desc}</p>
                  <ul className="space-y-1 mb-4">
                    {s.details.map((d) => (
                      <li key={d} className="text-xs text-gray-600 flex items-center gap-1">
                        <span className="text-green-500">✓</span> {d}
                      </li>
                    ))}
                  </ul>
                  <div className="bg-white rounded-xl px-3 py-2 border border-gray-100 inline-block">
                    <span className="text-xs text-gray-400">Desde </span>
                    <span className="font-bold text-blue-600">${s.priceFrom.toLocaleString()}</span>
                    <span className="text-xs text-gray-400"> — ${s.priceTo.toLocaleString()} MXN</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Price table */}
        <section className="bg-gray-50 py-16">
          <div className="max-w-4xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-3">Tabla de precios CDMX</h2>
            <p className="text-gray-500 text-center mb-8 text-sm">
              Precios de referencia del mercado privado en la Ciudad de México (2025). Los precios varían por colonia,
              tamaño del animal y clínica.
            </p>
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-900 text-white">
                      <th className="text-left px-4 py-3 font-semibold">Servicio</th>
                      <th className="text-right px-4 py-3 font-semibold">Mínimo</th>
                      <th className="text-right px-4 py-3 font-semibold">Máximo</th>
                      <th className="text-left px-4 py-3 font-semibold hidden sm:table-cell">Nota</th>
                    </tr>
                  </thead>
                  <tbody>
                    {PRICE_TABLE.map((row, i) => (
                      <tr key={row.service} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="px-4 py-3 font-medium text-gray-800">{row.service}</td>
                        <td className="px-4 py-3 text-right text-green-700 font-semibold">
                          {row.min === 0 ? "Gratis" : `$${row.min.toLocaleString()}`}
                        </td>
                        <td className="px-4 py-3 text-right text-gray-700">
                          {row.max === 0 ? "—" : `$${row.max.toLocaleString()}`}
                        </td>
                        <td className="px-4 py-3 text-gray-400 text-xs hidden sm:table-cell">{row.note}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="px-4 py-3 bg-blue-50 text-xs text-blue-700 border-t border-blue-100">
                💡 Fuentes: SpayMe CDMX 2024, Clínica Bienestar Tláhuac, Hospital Carson, VeterinariasCerca24.com.mx
              </div>
            </div>
          </div>
        </section>

        {/* How it works */}
        <section className="bg-white py-16">
          <div className="max-w-4xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">¿Cómo funciona?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { step: "1", icon: "🔍", title: "Busca", desc: "Encuentra veterinarios y paseadores verificados cerca de ti. Filtra por tipo de servicio, distancia y precio." },
                { step: "2", icon: "📅", title: "Reserva", desc: "Elige el proveedor, el servicio y el horario que mejor te convenga. Confirmación inmediata." },
                { step: "3", icon: "⭐", title: "Califica", desc: "Después del servicio, deja tu reseña. Ayudas a otros dueños a elegir con confianza." },
              ].map((s) => (
                <div key={s.step} className="text-center">
                  <div className="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center text-2xl mx-auto mb-4">
                    {s.icon}
                  </div>
                  <div className="text-xs font-bold text-blue-600 uppercase tracking-wide mb-1">Paso {s.step}</div>
                  <h3 className="font-semibold text-gray-900 text-lg mb-2">{s.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-blue-600 py-16 text-center text-white">
          <div className="max-w-2xl mx-auto px-4">
            <h2 className="text-3xl font-bold mb-4">¿Listo para empezar?</h2>
            <p className="text-blue-100 mb-8">Encuentra el veterinario perfecto para tu mascota hoy mismo.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/providers" className="bg-white text-blue-600 px-8 py-3 rounded-full font-semibold hover:bg-blue-50 transition">
                Buscar veterinarios
              </Link>
              <Link href="/providers/map" className="bg-blue-500 text-white border border-blue-400 px-8 py-3 rounded-full font-semibold hover:bg-blue-700 transition">
                Ver en el mapa 🗺️
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

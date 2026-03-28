import Link from "next/link";
import { PawPrint } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-2 text-white font-bold text-lg mb-3">
              <PawPrint className="w-5 h-5 text-blue-400" />
              PetCare
            </Link>
            <p className="text-sm leading-relaxed">
              Conectamos dueños de mascotas con veterinarios y paseadores de confianza cerca de ti.
            </p>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">Explorar</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/providers" className="hover:text-white transition">Todos los proveedores</Link></li>
              <li><Link href="/providers?type=VETERINARIAN" className="hover:text-white transition">Veterinarios</Link></li>
              <li><Link href="/providers?type=PET_WALKER" className="hover:text-white transition">Paseadores</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">Para Proveedores</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/register?role=provider" className="hover:text-white transition">Únete como proveedor</Link></li>
              <li><Link href="/dashboard/provider" className="hover:text-white transition">Panel de proveedor</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-semibold mb-3 uppercase tracking-wide">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/privacy" className="hover:text-white transition">Privacidad</Link></li>
              <li><Link href="/terms" className="hover:text-white transition">Términos de uso</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs">
          <p>© {new Date().getFullYear()} PetCare Marketplace. Todos los derechos reservados.</p>
          <p>Hecho con Next.js · Prisma · Vercel</p>
        </div>
      </div>
    </footer>
  );
}

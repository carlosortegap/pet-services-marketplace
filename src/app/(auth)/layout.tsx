import { PawPrint } from "lucide-react";
import Link from "next/link";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      <div className="p-6">
        <Link href="/" className="inline-flex items-center gap-2 text-blue-600 font-bold text-lg">
          <PawPrint className="w-5 h-5" />
          PetCare
        </Link>
      </div>
      <div className="flex-1 flex items-center justify-center px-4 py-8">
        {children}
      </div>
    </div>
  );
}

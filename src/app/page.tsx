export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-20">
        {/* Hero */}
        <div className="text-center mb-16">
          <div className="text-6xl mb-6">🐾</div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            PetCare Marketplace
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Find trusted veterinarians and pet walkers near you. Book appointments, track your pets health, and connect with the best pet care professionals.
          </p>
          <div className="flex gap-4 justify-center">
            <a href="/providers" className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-700 transition">
              Find a Provider
            </a>
            <a href="/register" className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-50 transition">
              Join as Provider
            </a>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl mb-4">🏥</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Veterinarians</h3>
            <p className="text-gray-600">Find certified vets nearby. Annual checkups, vaccinations, emergency care and more.</p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl mb-4">🦮</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Pet Walkers</h3>
            <p className="text-gray-600">Trusted walkers for your dog. Daily walks, group sessions, and overnight stays.</p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl mb-4">⭐</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Verified Reviews</h3>
            <p className="text-gray-600">Real reviews from pet owners. Book with confidence knowing providers are vetted.</p>
          </div>
        </div>

        {/* Stats */}
        <div className="bg-blue-600 rounded-3xl p-12 text-white text-center">
          <h2 className="text-3xl font-bold mb-8">Trusted by pet owners everywhere</h2>
          <div className="grid grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold">2,000+</div>
              <div className="text-blue-200 mt-1">Pet Owners</div>
            </div>
            <div>
              <div className="text-4xl font-bold">250+</div>
              <div className="text-blue-200 mt-1">Providers</div>
            </div>
            <div>
              <div className="text-4xl font-bold">4.8⭐</div>
              <div className="text-blue-200 mt-1">Avg Rating</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

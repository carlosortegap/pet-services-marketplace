/**
 * prisma/seed.ts
 * 6 test users: 3 owners + 2 vets + 1 walker
 *
 * Run:  npx prisma db seed
 * Credentials (all):  password = "password123"
 */

import { PrismaClient, UserRole, ProviderType, SubscriptionTier } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱  Seeding database…");

  const hash = await bcrypt.hash("password123", 10);

  // ── OWNERS ────────────────────────────────────────────────
  const owner1 = await prisma.user.upsert({
    where: { email: "sofia.ramirez@test.com" },
    update: {},
    create: {
      email: "sofia.ramirez@test.com",
      name: "Sofía Ramírez",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0001",
      ownerProfile: {
        create: {
          bio: "Dog mom × 2. Always looking for the best care for Luna and Frida.",
          city: "Polanco, CDMX",
          latitude: 19.4326,
          longitude: -99.1332,
          pets: {
            create: [
              { name: "Luna",  species: "dog", breed: "Golden Retriever", age: 3, weight: 28 },
              { name: "Frida", species: "dog", breed: "Chihuahua",        age: 6, weight: 2.5 },
            ],
          },
        },
      },
    },
  });

  const owner2 = await prisma.user.upsert({
    where: { email: "carlos.mendoza@test.com" },
    update: {},
    create: {
      email: "carlos.mendoza@test.com",
      name: "Carlos Mendoza",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0002",
      ownerProfile: {
        create: {
          city: "Roma Norte, CDMX",
          latitude: 19.4195,
          longitude: -99.1585,
          pets: {
            create: [
              { name: "Tobi", species: "cat", breed: "Siamese", age: 2, weight: 4 },
            ],
          },
        },
      },
    },
  });

  const owner3 = await prisma.user.upsert({
    where: { email: "ana.torres@test.com" },
    update: {},
    create: {
      email: "ana.torres@test.com",
      name: "Ana Torres",
      passwordHash: hash,
      role: UserRole.OWNER,
      phone: "+52-55-1001-0003",
      ownerProfile: {
        create: {
          city: "Condesa, CDMX",
          latitude: 19.4128,
          longitude: -99.1707,
          pets: {
            create: [
              { name: "Max",  species: "dog", breed: "Border Collie", age: 4, weight: 20 },
              { name: "Mimi", species: "rabbit", breed: "Holland Lop", age: 1, weight: 1.8 },
            ],
          },
        },
      },
    },
  });

  console.log(`  ✓  owners: ${owner1.name}, ${owner2.name}, ${owner3.name}`);

  // ── PROVIDERS ─────────────────────────────────────────────
  const vet1 = await prisma.user.upsert({
    where: { email: "dra.garcia@test.com" },
    update: {},
    create: {
      email: "dra.garcia@test.com",
      name: "Dra. María García",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0001",
      providerProfile: {
        create: {
          type: ProviderType.VETERINARIAN,
          displayName: "Dra. María García — Clínica Mascotas Felices",
          bio: "Veterinarian with 12 years of experience. Specialising in small animals, preventive care, and surgery. Fluent Spanish & English.",
          clinicName: "Clínica Mascotas Felices",
          address: "Av. Presidente Masaryk 123",
          city: "Polanco, CDMX",
          latitude: 19.4350,
          longitude: -99.1900,
          serviceRadius: 15,
          hourlyRate: 800,
          isVerified: true,
          isAvailable: true,
          rating: 4.9,
          reviewCount: 87,
          bookingCount: 210,
          specializations: {
            create: [
              { name: "Surgery" },
              { name: "Preventive care" },
              { name: "Dentistry" },
            ],
          },
          services: {
            create: [
              { name: "General Consultation", durationMinutes: 30, price: 400, description: "Full physical exam + diagnosis" },
              { name: "Vaccination", durationMinutes: 20, price: 250, description: "Core vaccines + certificate" },
              { name: "Dental Cleaning", durationMinutes: 60, price: 1200, description: "Under sedation, full oral health check" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 2, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 3, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 4, startTime: "09:00", endTime: "18:00" },
              { dayOfWeek: 5, startTime: "09:00", endTime: "15:00" },
            ],
          },
        },
      },
    },
  });

  const vet2 = await prisma.user.upsert({
    where: { email: "dr.hernandez@test.com" },
    update: {},
    create: {
      email: "dr.hernandez@test.com",
      name: "Dr. Javier Hernández",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0002",
      providerProfile: {
        create: {
          type: ProviderType.VETERINARIAN,
          displayName: "Dr. Javier Hernández — VetExpress Roma",
          bio: "Emergency vet and exotic animal specialist. 24/7 urgent care available. 8 years experience.",
          clinicName: "VetExpress Roma",
          address: "Calle Orizaba 88",
          city: "Roma Norte, CDMX",
          latitude: 19.4180,
          longitude: -99.1600,
          serviceRadius: 10,
          hourlyRate: 700,
          isVerified: true,
          isAvailable: true,
          rating: 4.7,
          reviewCount: 54,
          bookingCount: 130,
          specializations: {
            create: [
              { name: "Emergency care" },
              { name: "Exotic animals" },
              { name: "Internal medicine" },
            ],
          },
          services: {
            create: [
              { name: "Emergency Consultation", durationMinutes: 45, price: 600, description: "Urgent care, any hour" },
              { name: "General Checkup", durationMinutes: 30, price: 350, description: "Routine wellness exam" },
              { name: "Blood Panel", durationMinutes: 20, price: 500, description: "Full CBC + chemistry" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 2, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 3, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 4, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 5, startTime: "08:00", endTime: "22:00" },
              { dayOfWeek: 6, startTime: "10:00", endTime: "20:00" },
              { dayOfWeek: 0, startTime: "10:00", endTime: "18:00" },
            ],
          },
        },
      },
    },
  });

  const walker = await prisma.user.upsert({
    where: { email: "diego.walker@test.com" },
    update: {},
    create: {
      email: "diego.walker@test.com",
      name: "Diego López",
      passwordHash: hash,
      role: UserRole.PROVIDER,
      phone: "+52-55-2001-0003",
      providerProfile: {
        create: {
          type: ProviderType.PET_WALKER,
          displayName: "Diego López — PawWalks CDMX",
          bio: "Certified dog trainer and walker. Group and private walks in Condesa, Roma, and Polanco parks. GPS-tracked every session.",
          address: "Av. Ámsterdam 45",
          city: "Condesa, CDMX",
          latitude: 19.4100,
          longitude: -99.1750,
          serviceRadius: 8,
          hourlyRate: 200,
          isVerified: true,
          isAvailable: true,
          rating: 4.8,
          reviewCount: 112,
          bookingCount: 350,
          specializations: {
            create: [
              { name: "Dog training" },
              { name: "Group walks" },
              { name: "Puppy socialisation" },
            ],
          },
          services: {
            create: [
              { name: "30-min Solo Walk",   durationMinutes: 30, price: 150,  description: "One-on-one walk, GPS tracked" },
              { name: "60-min Solo Walk",   durationMinutes: 60, price: 250,  description: "Extended solo walk" },
              { name: "Group Walk (4 max)", durationMinutes: 60, price: 120,  description: "Socialise with other friendly dogs" },
              { name: "Puppy Training",     durationMinutes: 45, price: 350,  description: "Basic commands + leash manners" },
            ],
          },
          availability: {
            create: [
              { dayOfWeek: 1, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 2, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 3, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 4, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 5, startTime: "07:00", endTime: "19:00" },
              { dayOfWeek: 6, startTime: "08:00", endTime: "15:00" },
            ],
          },
        },
      },
    },
  });

  console.log(`  ✓  providers: ${vet1.name}, ${vet2.name}, ${walker.name}`);
  console.log("");
  console.log("🎉  Seed complete!");
  console.log("");
  console.log("  Test credentials (all passwords: password123)");
  console.log("  ┌─ OWNERS ──────────────────────────────────");
  console.log("  │  sofia.ramirez@test.com  (2 dogs)");
  console.log("  │  carlos.mendoza@test.com (1 cat)");
  console.log("  │  ana.torres@test.com     (1 dog + 1 rabbit)");
  console.log("  ├─ PROVIDERS ───────────────────────────────");
  console.log("  │  dra.garcia@test.com     (Vet · Polanco)");
  console.log("  │  dr.hernandez@test.com   (Vet · Roma)");
  console.log("  │  diego.walker@test.com   (Walker · Condesa)");
  console.log("  └───────────────────────────────────────────");
}

main()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(async () => { await prisma.$disconnect(); });

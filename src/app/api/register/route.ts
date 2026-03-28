import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { UserRole } from "@prisma/client";

export async function POST(req: NextRequest) {
  try {
    const { name, email, password, role } = await req.json();

    if (!name || !email || !password) {
      return NextResponse.json({ error: "Name, email and password are required." }, { status: 400 });
    }
    if (password.length < 8) {
      return NextResponse.json({ error: "Password must be at least 8 characters." }, { status: 400 });
    }

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      return NextResponse.json({ error: "An account with this email already exists." }, { status: 409 });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const userRole: UserRole = role === "PROVIDER" ? UserRole.PROVIDER : UserRole.OWNER;

    const user = await prisma.user.create({
      data: {
        name,
        email,
        passwordHash,
        role: userRole,
        ...(userRole === UserRole.OWNER
          ? { ownerProfile: { create: {} } }
          : { providerProfile: {
              create: {
                type: "VETERINARIAN",
                displayName: name,
                address: "",
                city: "",
                latitude: 0,
                longitude: 0,
              },
            }
          }),
      },
    });

    return NextResponse.json({ id: user.id, email: user.email, role: user.role }, { status: 201 });
  } catch (err) {
    console.error("[register]", err);
    return NextResponse.json({ error: "Internal server error." }, { status: 500 });
  }
}

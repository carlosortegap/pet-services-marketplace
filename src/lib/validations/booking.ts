import { z } from "zod";
import { BookingStatus } from "@prisma/client";

export const createBookingSchema = z.object({
  providerProfileId: z.string().cuid(),
  serviceId: z.string().cuid(),
  petId: z.string().cuid(),
  scheduledAt: z
    .string()
    .datetime()
    .refine((d) => new Date(d) > new Date(), {
      message: "Scheduled time must be in the future",
    }),
  notes: z.string().max(500).optional(),
});

export const updateBookingSchema = z.object({
  status: z.nativeEnum(BookingStatus),
  cancelReason: z.string().max(300).optional(),
});

export type CreateBookingInput = z.infer<typeof createBookingSchema>;
export type UpdateBookingInput = z.infer<typeof updateBookingSchema>;

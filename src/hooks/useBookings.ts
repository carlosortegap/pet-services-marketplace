import { useCallback, useState } from "react";
import type { CreateBookingInput } from "@/lib/validations/booking";

export function useBookings() {
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBookings = useCallback(async (status?: string) => {
    setLoading(true);
    try {
      const qs = status ? `?status=${status}` : "";
      const res = await fetch(`/api/bookings${qs}`);
      const data = await res.json();
      setBookings(data.bookings);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createBooking = useCallback(async (input: CreateBookingInput) => {
    const res = await fetch("/api/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error ?? "Failed to create booking");
    return data.booking;
  }, []);

  const updateBookingStatus = useCallback(async (id: string, status: string, cancelReason?: string) => {
    const res = await fetch(`/api/bookings/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, cancelReason }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error ?? "Failed to update booking");
    return data.booking;
  }, []);

  return { bookings, loading, error, fetchBookings, createBooking, updateBookingStatus };
}

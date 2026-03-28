export async function rateLimit(_identifier: string) {
  // Upstash Redis not configured yet — allow all requests
  return { success: true };
}

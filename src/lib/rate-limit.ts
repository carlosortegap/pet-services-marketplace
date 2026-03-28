import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(100, "15 m"),
  analytics: true,
});

export async function rateLimit(identifier: string) {
  return ratelimit.limit(identifier);
}

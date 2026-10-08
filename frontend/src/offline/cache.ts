import {
  getCache,
  setCache,
} from "./db";

const DEFAULT_CACHE_TIME =
  1000 * 60 * 60 * 24;

export async function cacheData<T>(
  key: string,
  data: T,
  ttl = DEFAULT_CACHE_TIME,
) {
  const expiresAt =
    new Date(
      Date.now() + ttl,
    ).toISOString();

  await setCache(
    key,
    data,
    expiresAt,
  );
}

export async function getCachedData<T>(
  key: string,
) {
  return getCache<T>(
    key,
  );
}

export async function cacheForever<T>(
  key: string,
  data: T,
) {
  await setCache(
    key,
    data,
  );
}

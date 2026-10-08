import {
  cacheData,
  getCachedData,
} from "../offline/cache";

import {
  enqueueRequest,
} from "../offline/queue";

import {
  isOnline,
} from "../offline/network";

const API_URL =
  import.meta.env
    .VITE_API_URL ||
  "http://localhost:8000/api";

export interface ApiOptions {
  method?:
    | "GET"
    | "POST"
    | "PUT"
    | "PATCH"
    | "DELETE";

  body?: unknown;

  cacheKey?: string;

  cacheTtl?: number;
}

export async function offlineApi<T>(
  endpoint: string,
  options: ApiOptions = {},
): Promise<T> {
  const method =
    options.method ||
    "GET";

  const cacheKey =
    options.cacheKey ||
    `${method}:${endpoint}`;

  if (
    method === "GET" &&
    !isOnline()
  ) {
    const cached =
      await getCachedData<T>(
        cacheKey,
      );

    if (
      cached !==
      undefined
    ) {
      return cached;
    }

    throw new Error(
      "This information is not available offline yet.",
    );
  }

  if (
    method !== "GET" &&
    !isOnline()
  ) {
    await enqueueRequest({
      entity:
        endpoint
          .split("/")
          .filter(Boolean)[0] ||
        "unknown",

      operation:
        method === "POST"
          ? "create"
          : method ===
              "DELETE"
            ? "delete"
            : "update",

      endpoint,

      method,

      body:
        options.body,
    });

    return {
      queued: true,
      offline: true,
    } as T;
  }

  const response =
    await fetch(
      `${API_URL}${endpoint}`,
      {
        method,

        headers: {
          "Content-Type":
            "application/json",
        },

        body:
          method === "GET"
            ? undefined
            : JSON.stringify(
                options.body,
              ),
      },
    );

  if (!response.ok) {
    const message =
      await response
        .text()
        .catch(
          () =>
            "Server request failed.",
        );

    throw new Error(
      message ||
        `Request failed with HTTP ${response.status}.`,
    );
  }

  const data =
    (await response.json()) as T;

  if (method === "GET") {
    await cacheData(
      cacheKey,
      data,
      options.cacheTtl,
    );
  }

  return data;
}

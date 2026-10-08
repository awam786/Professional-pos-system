import { offlineApi } from "../utils/offlineApi";

export const api = {
  get<T>(
    endpoint: string,
    cacheKey?: string,
  ) {
    return offlineApi<T>(
      endpoint,
      {
        method: "GET",
        cacheKey,
      },
    );
  },

  post<T>(
    endpoint: string,
    body?: unknown,
  ) {
    return offlineApi<T>(
      endpoint,
      {
        method: "POST",
        body,
      },
    );
  },

  put<T>(
    endpoint: string,
    body?: unknown,
  ) {
    return offlineApi<T>(
      endpoint,
      {
        method: "PUT",
        body,
      },
    );
  },

  patch<T>(
    endpoint: string,
    body?: unknown,
  ) {
    return offlineApi<T>(
      endpoint,
      {
        method: "PATCH",
        body,
      },
    );
  },

  delete<T>(
    endpoint: string,
  ) {
    return offlineApi<T>(
      endpoint,
      {
        method: "DELETE",
      },
    );
  },
};

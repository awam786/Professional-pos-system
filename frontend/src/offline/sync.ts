import {
  markCompleted,
  markFailed,
  markProcessing,
  pendingQueue,
} from "./queue";

import {
  isOnline,
} from "./network";

import type {
  SyncResult,
  SyncQueueItem,
} from "./types";

const API_URL =
  import.meta.env
    .VITE_API_URL ||
  "http://localhost:8000/api";

async function processItem(
  item: SyncQueueItem,
) {
  await markProcessing(item);

  try {
    const response =
      await fetch(
        `${API_URL}${item.endpoint}`,
        {
          method: item.method,

          headers: {
            "Content-Type":
              "application/json",
          },

          body:
            item.method ===
            "DELETE"
              ? undefined
              : JSON.stringify(
                  item.body,
                ),
        },
      );

    if (!response.ok) {
      const message =
        await response
          .text()
          .catch(
            () =>
              "Server rejected request.",
          );

      throw new Error(
        message ||
          `HTTP ${response.status}`,
      );
    }

    await markCompleted(item);

    return true;
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Synchronization failed.";

    await markFailed(
      item,
      message,
    );

    return false;
  }
}

export async function syncPendingRequests(): Promise<SyncResult> {
  if (!isOnline()) {
    return {
      success: false,
      processed: 0,
      failed: 0,
      remaining:
        (
          await pendingQueue()
        ).length,
      errors: [
        "Device is offline.",
      ],
    };
  }

  const items =
    await pendingQueue();

  let processed = 0;
  let failed = 0;

  const errors: string[] =
    [];

  for (const item of items) {
    const success =
      await processItem(
        item,
      );

    if (success) {
      processed++;
    } else {
      failed++;

      if (item.lastError) {
        errors.push(
          item.lastError,
        );
      }
    }
  }

  const remaining =
    (
      await pendingQueue()
    ).length;

  return {
    success:
      failed === 0,

    processed,

    failed,

    remaining,

    errors,
  };
}

let syncTimer:
  | ReturnType<typeof setInterval>
  | undefined;

export function startSyncEngine() {
  if (syncTimer) {
    return () => undefined;
  }

  syncTimer =
    setInterval(
      () => {
        if (isOnline()) {
          void syncPendingRequests();
        }
      },
      15000,
    );

  void syncPendingRequests();

  return () => {
    if (syncTimer) {
      clearInterval(
        syncTimer,
      );

      syncTimer = undefined;
    }
  };
}

import {
  addSyncQueueItem,
  deleteSyncQueueItem,
  getSyncQueue,
  updateSyncQueueItem,
} from "./db";

import type {
  SyncQueueItem,
} from "./types";

function createId() {
  if (
    typeof crypto !== "undefined" &&
    crypto.randomUUID
  ) {
    return crypto.randomUUID();
  }

  return (
    Date.now().toString(36) +
    Math.random()
      .toString(36)
      .slice(2)
  );
}

export async function enqueueRequest(
  input: Omit<
    SyncQueueItem,
    "id" | "createdAt" | "attempts" | "status"
  >,
) {
  const item: SyncQueueItem = {
    ...input,

    id: createId(),

    createdAt:
      new Date().toISOString(),

    attempts: 0,

    status: "pending",
  };

  await addSyncQueueItem(item);

  return item;
}

export async function pendingQueue() {
  const items =
    await getSyncQueue();

  return items
    .filter(
      (item) =>
        item.status === "pending" ||
        item.status === "failed",
    )
    .sort(
      (a, b) =>
        new Date(
          a.createdAt,
        ).getTime() -
        new Date(
          b.createdAt,
        ).getTime(),
    );
}

export async function markProcessing(
  item: SyncQueueItem,
) {
  await updateSyncQueueItem({
    ...item,

    status: "processing",

    attempts:
      item.attempts + 1,
  });
}

export async function markFailed(
  item: SyncQueueItem,
  error: string,
) {
  await updateSyncQueueItem({
    ...item,

    status: "failed",

    lastError: error,
  });
}

export async function markCompleted(
  item: SyncQueueItem,
) {
  await deleteSyncQueueItem(
    item.id,
  );
}

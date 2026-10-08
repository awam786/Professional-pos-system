import {
  DBSchema,
  IDBPDatabase,
  openDB,
} from "idb";

import type {
  CachedResponse,
  OfflineRecord,
  SyncQueueItem,
} from "./types";

interface POSDatabase extends DBSchema {
  records: {
    key: string;
    value: OfflineRecord;
    indexes: {
      "by-entity": string;
      "by-sync": number;
    };
  };

  syncQueue: {
    key: string;
    value: SyncQueueItem;
    indexes: {
      "by-status": string;
      "by-created": string;
    };
  };

  cache: {
    key: string;
    value: CachedResponse;
  };
}

const DB_NAME = "professional-pos-db";

const DB_VERSION = 1;

let databasePromise:
  | Promise<IDBPDatabase<POSDatabase>>
  | undefined;

export function getDatabase() {
  if (!databasePromise) {
    databasePromise = openDB<
      POSDatabase
    >(
      DB_NAME,
      DB_VERSION,
      {
        upgrade(db) {
          if (!db.objectStoreNames.contains("records")) {
            const store =
              db.createObjectStore(
                "records",
                {
                  keyPath: "id",
                },
              );

            store.createIndex(
              "by-entity",
              "entity",
            );

            store.createIndex(
              "by-sync",
              "synced",
            );
          }

          if (
            !db.objectStoreNames.contains(
              "syncQueue",
            )
          ) {
            const store =
              db.createObjectStore(
                "syncQueue",
                {
                  keyPath: "id",
                },
              );

            store.createIndex(
              "by-status",
              "status",
            );

            store.createIndex(
              "by-created",
              "createdAt",
            );
          }

          if (
            !db.objectStoreNames.contains(
              "cache",
            )
          ) {
            db.createObjectStore(
              "cache",
              {
                keyPath: "key",
              },
            );
          }
        },
      },
    );
  }

  return databasePromise;
}

export async function saveOfflineRecord(
  record: OfflineRecord,
) {
  const db = await getDatabase();

  await db.put(
    "records",
    record,
  );
}

export async function getOfflineRecord(
  id: string,
) {
  const db = await getDatabase();

  return db.get(
    "records",
    id,
  );
}

export async function deleteOfflineRecord(
  id: string,
) {
  const db = await getDatabase();

  await db.delete(
    "records",
    id,
  );
}

export async function getRecordsByEntity(
  entity: string,
) {
  const db = await getDatabase();

  return db.getAllFromIndex(
    "records",
    "by-entity",
    entity,
  );
}

export async function addSyncQueueItem(
  item: SyncQueueItem,
) {
  const db = await getDatabase();

  await db.put(
    "syncQueue",
    item,
  );
}

export async function getSyncQueue() {
  const db = await getDatabase();

  return db.getAll(
    "syncQueue",
  );
}

export async function deleteSyncQueueItem(
  id: string,
) {
  const db = await getDatabase();

  await db.delete(
    "syncQueue",
    id,
  );
}

export async function updateSyncQueueItem(
  item: SyncQueueItem,
) {
  const db = await getDatabase();

  await db.put(
    "syncQueue",
    item,
  );
}

export async function setCache<T>(
  key: string,
  data: T,
  expiresAt?: string,
) {
  const db = await getDatabase();

  await db.put(
    "cache",
    {
      key,
      data,
      createdAt:
        new Date().toISOString(),
      expiresAt,
    },
  );
}

export async function getCache<T>(
  key: string,
): Promise<T | undefined> {
  const db = await getDatabase();

  const cached =
    await db.get(
      "cache",
      key,
    );

  if (!cached) {
    return undefined;
  }

  if (
    cached.expiresAt &&
    new Date(cached.expiresAt)
      .getTime() <
      Date.now()
  ) {
    await db.delete(
      "cache",
      key,
    );

    return undefined;
  }

  return cached.data as T;
}

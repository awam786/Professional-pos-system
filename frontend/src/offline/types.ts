export type SyncOperation =
  | "create"
  | "update"
  | "delete";

export type SyncStatus =
  | "pending"
  | "processing"
  | "completed"
  | "failed";

export interface OfflineRecord<T = unknown> {
  id: string;

  entity: string;

  operation: SyncOperation;

  data: T;

  createdAt: string;

  updatedAt: string;

  version: number;

  synced: boolean;
}

export interface SyncQueueItem {
  id: string;

  entity: string;

  operation: SyncOperation;

  endpoint: string;

  method:
    | "POST"
    | "PUT"
    | "PATCH"
    | "DELETE";

  body?: unknown;

  createdAt: string;

  attempts: number;

  status: SyncStatus;

  lastError?: string;

  processedAt?: string;
}

export interface CachedResponse<T = unknown> {
  key: string;

  data: T;

  createdAt: string;

  expiresAt?: string;
}

export interface SyncResult {
  success: boolean;

  processed: number;

  failed: number;

  remaining: number;

  errors: string[];
}

export interface NetworkState {
  online: boolean;

  lastOnlineAt?: string;

  lastOfflineAt?: string;
}

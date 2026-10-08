import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getSyncQueue,
} from "../offline/db";

import {
  syncPendingRequests,
} from "../offline/sync";

export interface SyncState {
  pending: number;
  syncing: boolean;
  lastSync?: string;
  lastError?: string;
}

export function useSyncStatus() {
  const [
    state,
    setState,
  ] = useState<SyncState>({
    pending: 0,
    syncing: false,
  });

  const refresh =
    useCallback(
      async () => {
        const queue =
          await getSyncQueue();

        setState(
          (current) => ({
            ...current,
            pending:
              queue.length,
          }),
        );
      },
      [],
    );

  const sync =
    useCallback(
      async () => {
        setState(
          (current) => ({
            ...current,
            syncing: true,
            lastError:
              undefined,
          }),
        );

        try {
          const result =
            await syncPendingRequests();

          setState({
            pending:
              result.remaining,

            syncing: false,

            lastSync:
              new Date().toISOString(),

            lastError:
              result.errors.length
                ? result.errors[0]
                : undefined,
          });
        } catch (error) {
          setState(
            (current) => ({
              ...current,
              syncing: false,
              lastError:
                error instanceof
                Error
                  ? error.message
                  : "Synchronization failed.",
            }),
          );
        }
      },
      [],
    );

  useEffect(() => {
    void refresh();

    const timer =
      setInterval(
        () => {
          void refresh();
        },
        3000,
      );

    return () =>
      clearInterval(timer);
  }, [refresh]);

  return {
    ...state,
    refresh,
    sync,
  };
}

import {
  Cloud,
  CloudOff,
  RefreshCw,
} from "lucide-react";

import {
  useOnlineStatus,
} from "../hooks/useOnlineStatus";

import {
  useSyncStatus,
} from "../hooks/useSyncStatus";

export default function SyncStatus() {
  const {
    online,
  } = useOnlineStatus();

  const {
    pending,
    syncing,
    sync,
  } = useSyncStatus();

  return (
    <button
      type="button"
      onClick={() => {
        if (online && !syncing) {
          void sync();
        }
      }}
      disabled={
        !online ||
        syncing
      }
      title={
        !online
          ? "Offline"
          : pending > 0
            ? `${pending} changes waiting to sync`
            : "Data synchronized"
      }
      style={{
        display: "flex",
        alignItems: "center",
        gap: 7,
        border: "1px solid #27272a",
        background: "#18181b",
        color: "#d4d4d8",
        borderRadius: 8,
        padding: "7px 10px",
        cursor:
          online && !syncing
            ? "pointer"
            : "default",
      }}
    >
      {online ? (
        <Cloud size={15} />
      ) : (
        <CloudOff size={15} />
      )}

      <span>
        {syncing
          ? "Syncing..."
          : pending > 0
            ? `${pending} pending`
            : "Synced"}
      </span>

      {online &&
        pending > 0 && (
          <RefreshCw
            size={14}
            style={{
              animation: syncing
                ? "spin 1s linear infinite"
                : undefined,
            }}
          />
        )}
    </button>
  );
}

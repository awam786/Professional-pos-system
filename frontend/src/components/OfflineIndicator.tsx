import {
  CloudOff,
  Wifi,
} from "lucide-react";

import {
  useOnlineStatus,
} from "../hooks/useOnlineStatus";

export default function OfflineIndicator() {
  const {
    online,
  } = useOnlineStatus();

  if (online) {
    return (
      <div
        style={{
          position: "fixed",
          bottom: 16,
          left: 16,
          zIndex: 9999,
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "8px 12px",
          borderRadius: 8,
          background: "#18181b",
          color: "#a1a1aa",
          fontSize: 12,
          border: "1px solid #27272a",
        }}
      >
        <Wifi size={14} />
        Online
      </div>
    );
  }

  return (
    <div
      style={{
        position: "fixed",
        bottom: 16,
        left: 16,
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        gap: 8,
        padding: "9px 13px",
        borderRadius: 8,
        background: "#7f1d1d",
        color: "#fecaca",
        fontSize: 12,
        fontWeight: 600,
        border: "1px solid #991b1b",
      }}
    >
      <CloudOff size={14} />
      Offline — changes will sync automatically
    </div>
  );
}

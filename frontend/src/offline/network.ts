import type {
  NetworkState,
} from "./types";

let state: NetworkState = {
  online:
    typeof navigator ===
    "undefined"
      ? true
      : navigator.onLine,
};

const listeners =
  new Set<
    (state: NetworkState) => void
  >();

function update(
  online: boolean,
) {
  const now =
    new Date().toISOString();

  state = {
    online,

    lastOnlineAt: online
      ? now
      : state.lastOnlineAt,

    lastOfflineAt: online
      ? state.lastOfflineAt
      : now,
  };

  listeners.forEach(
    (listener) =>
      listener(state),
  );
}

if (
  typeof window !==
  "undefined"
) {
  window.addEventListener(
    "online",
    () => update(true),
  );

  window.addEventListener(
    "offline",
    () => update(false),
  );
}

export function isOnline() {
  return state.online;
}

export function getNetworkState() {
  return {
    ...state,
  };
}

export function subscribeNetwork(
  listener: (
    state: NetworkState,
  ) => void,
) {
  listeners.add(listener);

  listener({
    ...state,
  });

  return () => {
    listeners.delete(
      listener,
    );
  };
}

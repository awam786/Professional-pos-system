import {
  useEffect,
  useState,
} from "react";

import {
  getNetworkState,
  subscribeNetwork,
} from "../offline/network";

export function useOnlineStatus() {
  const [
    network,
    setNetwork,
  ] = useState(
    getNetworkState(),
  );

  useEffect(() => {
    return subscribeNetwork(
      setNetwork,
    );
  }, []);

  return network;
}

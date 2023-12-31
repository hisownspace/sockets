import { createContext, useEffect, useState } from "react";

export const SessionContext = createContext();

export function SessionProvider(props) {
  const [session, setSession] = useState({ user: null });

  return (
    <SessionContext.Provider value={{ session, setSession }}>
      {props.children}
    </SessionContext.Provider>
  );
}

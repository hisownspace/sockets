import { createContext, useState } from "react";

export const ConversationContext = createContext();

export function ConversationProvider(props) {
  const [conversations, setConversations] = useState([]);

  return (
    <ConversationContext.Provider value={{ conversations, setConversations }}>
      {props.children}
    </ConversationContext.Provider>
  );
}

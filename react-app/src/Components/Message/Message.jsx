import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import { SessionContext } from "../../context/session";

export default function Message() {
  const { session } = useContext(SessionContext);
  const [dmInputValue, setDMInputValue] = useState("");
  const { conversationId } = useParams();
  const [conversation, setConversation] = useState({});

  useEffect(() => {
    const thisConversation = session.conversations.find(
      (conversation) => conversation.id == conversationId
    );
    setConversation(thisConversation);
    console.log(thisConversation);
  }, [conversationId]);

  const handleChange = (e) => {
    setDMInputValue(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("hello!");
    const res = await fetch(`/api/conversations/${conversationId}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: session.id, content: dmInputValue }),
    });
    if (res.ok) {
      const message = await res.json();
    } else {
      const errors = await res.json();
      console.log(errors);
    }
  };

  return (
    <div className="dm-container">
      <h1>
        {conversation.members?.map((member, idx) =>
          idx + 1 < conversation.members.length ? `${member}, ` : member
        )}
      </h1>
      {conversation.messages?.map((message, idx) => (
        <div key={idx} className="chat-message">
          {message.new_day ? (
            <div className="new-day-container">
              <span>{message.new_day}</span>
            </div>
          ) : null}
          <div className="message-content" id={`message-content-${message.id}`}>
            {message.content}
          </div>
          <div className="message-user">
            <span>
              <span style={{ color: message.user.theme }}>
                {message.user.username}
              </span>
              <span className="timestamp">{message.created_at}</span>
            </span>
          </div>
        </div>
      ))}
      <form onSubmit={handleSubmit} className="dm-chat-form">
        <input
          className="dm-input"
          value={dmInputValue}
          onChange={handleChange}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

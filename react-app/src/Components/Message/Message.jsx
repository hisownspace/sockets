import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import { SessionContext } from "../../context/session";

export default function Message({ socket }) {
  const { session } = useContext(SessionContext);
  const [dmInputValue, setDMInputValue] = useState("");
  const { conversationId } = useParams();
  const [conversation, setConversation] = useState({});

  useEffect(() => {
    if (socket) {
      socket.on("chat", () => {
        console.log("prop drilling works");
      });
    }
  }, [socket]);

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

  useEffect(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
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

  useEffect(() => {
    console.log(conversation.messages);
    if (conversation.messages?.length) {
      const latestMessage =
        conversation.messages[conversation.messages?.length - 1];
      const now = Date.now();
      const time = new Date(latestMessage["updated_at"]).getTime();
      if (
        now - time < 1000 &&
        session.id != latestMessage.user.id &&
        !document.hidden
      ) {
        const newMessage = document.getElementById(
          `direct-message-content-${latestMessage.id}`
        );
        newMessage.style.animation = "blinker 2s linear 1";
      }
    }
  }, [conversation.messages]);

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
          <div
            className="message-content"
            id={`direct-message-content-${message.id}`}
          >
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

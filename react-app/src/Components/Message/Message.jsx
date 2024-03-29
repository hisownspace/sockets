import { useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router";
import { useLocation } from "react-router-dom";
import { SessionContext } from "../../context/session";

export default function Message({ socket }) {
  const { session, setSession } = useContext(SessionContext);
  const navigate = useNavigate();
  const [dmInputValue, setDMInputValue] = useState("");
  const { conversationId } = useParams();
  const [messages, setMessages] = useState([]);
  const [members, setMembers] = useState([]);
  const [chatErrors, setChatErrors] = useState([]);
  const location = useLocation();

  useEffect(() => {
    if (location.state) {
      const new_message = document.getElementById(
        `direct-message-content-${location.state}`,
      );
      if (new_message) {
        new_message.style.animation = "blinker 2s linear 1";
      }
    }
  }, [location, messages]);

  useEffect(() => {
    const thisConversation = session.conversations.find(
      (conversation) => conversation.id == conversationId,
    );
    if (thisConversation) {
      thisConversation.members = thisConversation.members.filter(
        (member) => member != session.username,
      );
      if (
        thisConversation.members[thisConversation.members.length - 1] !==
        session.username
      ) {
        thisConversation.members.push(session.username);
      }
      setMessages(thisConversation.messages);
      setMembers(thisConversation.members);
    } else if (session.conversations) {
      navigate("/1");
    }
  }, [session]);

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
      setDMInputValue("");
      setChatErrors([]);
    } else {
      const data = await res.json();
      if (data.csrf_token) {
        data.csrf_token += " Please send your message again.";
      }
      setChatErrors(Object.values(data));
    }
  };

  useEffect(() => {
    if (messages.length) {
      const latestMessage = messages[messages.length - 1];
      const now = Date.now();
      const time = new Date(latestMessage["updated_at"]).getTime();
      if (
        now - time < 100 &&
        session.id != latestMessage.user.id &&
        !document.hidden
      ) {
        const newMessage = document.getElementById(
          `direct-message-content-${latestMessage.id}`,
        );
        newMessage.style.animation = "blinker 2s linear 1";
      }
    }
  }, [messages, session]);

  return (
    <div className="dm-container">
      <h1>
        {members.map((member, idx) =>
          idx + 1 < members.length
            ? session.username === member
              ? "You, "
              : `${member}, `
            : session.username === member
            ? "You"
            : member,
        )}
      </h1>
      {messages.map((message, idx) => (
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
                {message.user.username == session.username
                  ? "You"
                  : message.user.username}
              </span>
              <span className="timestamp">{message.created_at}</span>
            </span>
          </div>
        </div>
      ))}
      <ul className="errors">
        {chatErrors.map((error, idx) => (
          <li key={idx}>{error}</li>
        ))}
      </ul>
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

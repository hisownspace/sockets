import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import addNotification from "react-push-notification";
import { SessionContext } from "../../context/session";
import { socket } from "../../context/socket";

export default function Room() {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const { session } = useContext(SessionContext);
  const { roomId } = useParams();
  const [roomName, setRoomName] = useState("");

  useEffect(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });

  useEffect(() => {
    (async () => {
      const res = await fetch(`/api/rooms/${roomId}`);
      if (res.ok) {
        const data = await res.json();
        setRoomName(data.name);
        setMessages(data.messages);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();

    socket.emit("join", roomId);

    const onRoomMessage = (chat) => {
      console.log("emitting chat");
      setMessages((messages) => [...messages, chat]);
      console.log(chat);
      if (session.id != chat.user.id && !document.hasFocus()) {
        addNotification({
          title: chat.room,
          subtitle: { id: `message-content-${chat.id}` },
          icon: "../../../public/vite.jpg",
          message: `${chat.user.username}: ${chat.content}`,
          native: true,
          onClick: handleNotificationClick,
          silent: false,
          badge: ["test"],
        });
      }
    };

    socket.on("chat", onRoomMessage);

    return () => {
      socket.off("chat", onRoomMessage);
    };
  }, [roomId]);

  const handleNotificationClick = (e) => {
    window.focus();
    const new_message = document.getElementById(e.target.data.id);
    new_message.style.animation = "blinker 2s linear 1";
    window.scrollTo(0, document.body.scrollHeight);
  };

  const updateMessageInput = (e) => {
    setMessageInput(e.target.value);
  };

  const sendMessage = (e) => {
    e.preventDefault();
    socket.emit("chat", {
      user: session.username,
      user_id: session.id,
      content: messageInput,
      room_id: roomId,
    });
    setMessageInput("");
  };

  useEffect(() => {
    if (messages.length) {
      const latestMessage = messages[messages.length - 1];
      const now = Date.now();
      const time = new Date(latestMessage["updated_at"]).getTime();
      if (
        now - time < 1000 &&
        session.id != latestMessage.user.id &&
        !document.hidden
      ) {
        const newMessage = document.getElementById(
          `message-content-${latestMessage.id}`
        );
        newMessage.style.animation = "blinker 2s linear 1";
      }
    }
  }, [messages]);

  return (
    <div className="chat-room-container">
      <div>
        <div className="room-greeting">
          <h1>Welcome to {roomName}!</h1>
        </div>
        <div className="message-container">
          {messages.map((message, idx) => (
            <div key={idx} className="chat-message">
              {message.new_day ? (
                <div className="new-day-container">
                  <span>{message.new_day}</span>
                </div>
              ) : null}
              <div
                className="message-content"
                id={`message-content-${message.id}`}
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
        </div>
        <div className="message-input">
          <form className="message-form" onSubmit={sendMessage}>
            <input value={messageInput} onChange={updateMessageInput} />
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
  );
}

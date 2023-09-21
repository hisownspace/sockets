import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import { io } from "socket.io-client";
import addNotification from "react-push-notification";
import { SessionContext } from "../../context/session";

let socket;

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
    socket = io("http://127.0.0.1:5000", {
      transports: ["polling", "websocket"],
    });
    console.log("in socket useEffect");

    socket.emit("join", roomId);

    // callback to check the connection type
    socket.on("connect", () => {
      const transport = socket.io.engine.transport.name;
      console.log(transport);
      const connected = socket.connected;
      console.log(connected);
    });

    // runs if/when the connection is upgraded from polling to websockets
    socket.io.engine.on("upgrade", () => {
      const upgradedTransport = socket.io.engine.transport.name;
      console.log(upgradedTransport);
    });

    socket.on("chat", (chat) => {
      console.log("emitting chat");
      setMessages((messages) => [...messages, chat]);
      console.log(chat);
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
    });

    return () => {
      console.log("connection closed");
      socket.disconnect();
    };
  }, [roomId]);

  const handleNotificationClick = (e) => {
    window.focus();
    const new_message = document.getElementById(e.target.data.id);
    new_message.style.animation = "blinker 2s linear 3";
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
                    {message.user.username}
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

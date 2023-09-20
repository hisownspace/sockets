import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router";
import { io } from "socket.io-client";
import { SessionContext } from "../../context/session";

let socket;

export default function Room() {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const { session } = useContext(SessionContext);
  const { roomId } = useParams();
  const [roomName, setRoomName] = useState("");

  useEffect(() => {
    (async () => {
      const res = await fetch(`/api/rooms/${roomId}`);
      if (res.ok) {
        const data = await res.json();
        setRoomName(data.name);
        console.log(data.name);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();
  }, [roomId]);

  useEffect(() => {
    socket = io("ws://127.0.0.1:5000", {
      transports: ["polling", "websocket"],
    });
    console.log("in socket useEffect");

    socket.on("connect", () => {
      const transport = socket.io.engine.transport.name;
      console.log(transport);
      const connected = socket.connected;
      console.log(connected);
    });

    socket.on("chat", (chat) => {
      console.log("emitting chat");
      setMessages((messages) => [...messages, chat]);
    });

    return () => {
      console.log("connection closed");
      socket.disconnect();
    };
  }, []);

  const updateMessageInput = (e) => {
    setMessageInput(e.target.value);
  };

  const sendMessage = (e) => {
    e.preventDefault();
    socket.emit("chat", { user: session.username, content: messageInput });
    setMessageInput("");
  };

  return (
    <div className="chat-room-container">
      <h1>Welcome to {roomName}!</h1>
      <div className="message-container">
        {messages.map((message, idx) => (
          <div key={idx} className="chat-message">
            <div className="message-content">{message.content}</div>
            <div className="message-user">
              <span>{message.user}</span>
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
  );
}

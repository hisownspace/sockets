import { useEffect, useState } from "react";
import { useParams } from "react-router";

export default function Room() {
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

  return (
    <div className="chat-room-container">
      <h1>Welcome to {roomName}!</h1>
    </div>
  );
}

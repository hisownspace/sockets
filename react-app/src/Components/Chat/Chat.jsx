import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";

export default function Chat() {
  const [rooms, setRooms] = useState([]);
  useEffect(() => {
    (async () => {
      const res = await fetch("/api/rooms");
      if (res.ok) {
        const allRooms = await res.json();
        setRooms(allRooms);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();
    (async () => {
      const res = await fetch("/api/messages");
      if (res.ok) {
        const allConversations = await res.json();
      }
    })();
  }, []);

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <h3 className="sidebar-title">Rooms</h3>
        <ul>
          {rooms.map((room) => (
            <li className="room-list-item" key={room.id}>
              <Link to={`/${room.id}`}>{room.name}</Link>
            </li>
          ))}
        </ul>
        <h3 className="sidebar-title">Messages</h3>
      </div>
      <Outlet />
    </div>
  );
}

import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";
import NewDirectMessageModal from "../NewDirectMessageModal";

export default function Chat() {
  const [rooms, setRooms] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [open, setOpen] = useState(false);

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
      const res = await fetch("/api/conversations");
      if (res.ok) {
        const allConversations = await res.json();
      }
    })();
  }, []);

  const newConversation = (e) => {
    e.preventDefault();
    console.log("Open modal");
    setOpen(true);
  };

  return (
    <div className="chat-container" id="modal-parent">
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
        <form onSubmit={newConversation} className="dm-form">
          <button className="dm-button">New Conversation</button>
        </form>
      </div>
      <ul>
        {conversations.map((conversation) => {
          <li className="conversation-list-item" key={conversation.id}>
            <Link to={`/conversation/${conversation.id}`}>
              {conversation.members.map((member, idx) =>
                idx < conversation.members.length ? `${member},` : { member }
              )}
            </Link>
          </li>;
        })}
      </ul>
      <Outlet />
      <div>
        <NewDirectMessageModal isOpen={open} onClose={() => setOpen(false)} />
      </div>
    </div>
  );
}

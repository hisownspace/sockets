import { useContext, useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";
import NewDirectMessageModal from "../NewDirectMessageModal";
import { SessionContext } from "../../context/session";
import { socket } from "../../context/socket";

export default function Chat() {
  const { session } = useContext(SessionContext);
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
        let allConversations = await res.json();
        allConversations = allConversations.filter(
          (convo) => convo.messages.length
        );
        setConversations(allConversations);
        console.log(allConversations);
      }
    })();
  }, []);

  const handleDirectMessage = async (chat) => {
    const res = await fetch("/api/conversations");
    if (res.ok) {
      const allConversations = await res.json();
      setConversations(allConversations);
    }
  };

  socket.on("dm", handleDirectMessage);

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
        <ul>
          {conversations.map((conversation) => (
            <li className="conversation-list-item" key={conversation.id}>
              <Link to={`/conversations/${conversation.id}`}>
                {conversation.members.map((member, idx) =>
                  idx + 1 < conversation.members.length &&
                  !(
                    conversation.members[conversation.members.length - 1] ==
                      session.username &&
                    idx + 2 === conversation.members.length
                  )
                    ? session.username === member
                      ? null
                      : conversation.members.length === 2
                      ? member
                      : `${member}, `
                    : session.username === member
                    ? null
                    : `${member}`
                )}
              </Link>
            </li>
          ))}
        </ul>
      </div>
      <Outlet />
      <div>
        <NewDirectMessageModal
          isOpen={open}
          onClose={() => setOpen(false)}
          setConversations={setConversations}
        />
      </div>
    </div>
  );
}

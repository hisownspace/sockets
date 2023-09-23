import { useContext, useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";
import { Route, Routes, useNavigate } from "react-router-dom";
import addNotification from "react-push-notification";
import Login from "./Components/Login";
import Chat from "./Components/Chat";
import Room from "./Components/Room";
import { SessionContext } from "./context/session";
import Message from "./Components/Message";

let socket;

function App() {
  const { session, setSession } = useContext(SessionContext);
  const navigate = useNavigate();
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    (async () => {
      const res = await fetch("/api/auth");
      if (res.ok) {
        const user = await res.json();
        setSession(user);
        setLoaded(true);
      } else {
        console.log(await res.json());
        setLoaded(false);
        // return navigate("/");
      }
      return () => setLoaded(false);
    })();
  }, [navigate]);

  const handleNotificationClick = (e) => {
    // window.focus();
    const convo_id = e.target.data.convo_id;
    const id = e.target.data.message_id;
    console.log(id);
    navigate(`/conversations/${convo_id}`, { state: id });
    window.scrollTo(0, document.body.scrollHeight);
  };

  useEffect(() => {
    socket = io("http://127.0.0.1:5000", {
      transports: ["websocket", "polling"],
    });

    for (let i = 0; i < session.conversations?.length; i++) {
      socket.emit("join", `conversation/${session.conversations[i].id}`);
    }
    socket.on("dm", (chat) => {
      // console.log(session);
      const conversation = session.conversations?.find(
        (convo) => convo.id == chat.conversation_id
      );
      const convoIdx = session.conversations?.indexOf(
        (convo) => convo.id == chat.conversation_id
      );

      const newSession = { ...session };

      console.log(conversation);
      conversation?.messages.push(chat);
      newSession.conversations[convoIdx] = conversation;
      // console.log(conversation?.messages);
      setSession(newSession);
      addNotification({
        title: chat.room,
        subtitle: { convo_id: chat.conversation_id, message_id: chat.id },
        icon: "../../../public/vite.jpg",
        message: `${chat.user.username}: ${chat.content}`,
        native: true,
        onClick: handleNotificationClick,
        silent: false,
        badge: ["test"],
      });
    });
    return () => {
      socket.disconnect();
    };
  }, [session]);

  return (
    <>
      <Login />
      {loaded ? (
        <Routes>
          <Route path="/" element={<Chat />}>
            <Route path=":roomId" element={<Room />} />
            <Route
              path="conversations/:conversationId"
              element={<Message />}
              // socket={socket}
            />
          </Route>
        </Routes>
      ) : null}
    </>
  );
}

export default App;

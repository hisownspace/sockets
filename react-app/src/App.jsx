import { useContext, useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";
import { Route, Routes, useNavigate } from "react-router-dom";
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

  useEffect(() => {
    socket = io("http://127.0.0.1:5000", {
      transports: ["websocket", "polling"],
    });

    socket.emit("join", "conversation/2");
  }, []);

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
              socket={socket}
            />
          </Route>
        </Routes>
      ) : null}
    </>
  );
}

export default App;

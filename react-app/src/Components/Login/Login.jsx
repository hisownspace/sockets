import { useContext, useEffect, useState } from "react";
import { SessionContext } from "../../context/session";
import { useNavigate } from "react-router";
import { socket } from "../../context/socket";
import { ConversationContext } from "../../context/conversations";

export default function Login() {
  const navigate = useNavigate();
  const { session, setSession } = useContext(SessionContext);
  const { setConversations } = useContext(ConversationContext);
  const [currentUser, setCurrentUser] = useState();
  const [allUsers, setAllUsers] = useState([]);
  const [errors, setErrors] = useState({});
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("password");

  useEffect(() => {
    (async () => {
      const res = await fetch("/api/users");
      if (res.ok) {
        const users = await res.json();
        setAllUsers(users);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();
  }, []);

  useEffect(() => {
    setUsername(allUsers[0]?.username);
  }, [allUsers]);

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      const user = await res.json();
      setSession(user);
      socket.connect();
      navigate("/1");
    } else {
      const errors = await res.json();
      console.log(errors);
    }
  };

  const handleLogout = (e) => {
    e.preventDefault();
    (async () => {
      const res = await fetch("/api/auth/logout");
      if (res.ok) {
        setSession({});
        navigate("/");
        socket.disconnect();
      }
    })();
  };

  return session.username ? (
    <div className="logout-container">
      <div>
        <div className="user-greeting">Hello {session.username}!</div>
        <form onSubmit={handleLogout}>
          <button>Log Out</button>
        </form>
      </div>
    </div>
  ) : (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <p>
          <select
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          >
            {allUsers.map((user) => (
              <option key={user.id}>{user.username}</option>
            ))}
          </select>
        </p>
        <button>Log In</button>
      </form>
    </div>
  );
}

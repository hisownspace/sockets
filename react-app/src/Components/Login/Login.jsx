import { useContext, useEffect, useState } from "react";
import { SessionContext } from "../../context/session";
import { useNavigate } from "react-router";

export default function Login() {
  const navigate = useNavigate();
  const { session, setSession } = useContext(SessionContext);
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
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      const user = await res.json();
      setSession(user);
    } else {
      const errors = await res.json();
      console.log(errors);
    }
  };

  const handleLogout = () => {
    setSession();
  };

  return session ? (
    <div className="logout-container">
      <div>
        <p>Hello {session?.user?.username}!</p>
        <form onSubmit={handleLogout}>
          <button>Logout</button>
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
        <button>Submit</button>
      </form>
    </div>
  );
}

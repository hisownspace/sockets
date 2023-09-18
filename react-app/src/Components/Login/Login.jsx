import { useEffect, useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    console.log("Hitting login route!");
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    console.log("logging in...");
    const loginInfo = fetch("/api/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: { username, password },
    });
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <p>
          <label htmlFor="username">Username: </label>
          <input
            value={username}
            id="username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </p>
        <p>
          <label htmlFor="password">Password: </label>
          <input
            value={password}
            id="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </p>
        <button>Submit</button>
      </form>
    </div>
  );
}

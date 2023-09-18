import { useEffect, useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    console.log("Hitting login route!");
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    console.log("logging in...");
    const loginInfo = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    console.log(await loginInfo.json());
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <p>
          <label htmlFor="username">Username: </label>
          <input
            value={username}
            id="username"
            type="text"
            onChange={(e) => setUsername(e.target.value)}
          />
        </p>
        <p>
          <label htmlFor="password">Password: </label>
          <input
            value={password}
            id="password"
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </p>
        <button>Submit</button>
      </form>
    </div>
  );
}

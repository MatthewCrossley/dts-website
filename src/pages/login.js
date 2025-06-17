import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { setAuth } from "../utils/auth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  let navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("https://human-canidae-matthewcrossley-75876ff3.koyeb.app/users/current", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Basic ${btoa(`${username}:${password}`)}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setAuth(userData);
        navigate("/");
      } else {
        document.querySelector(".error-message").textContent =
          "Invalid username or password";
      }
    } catch (error) {
      document.querySelector(".error-message").textContent = "Error: " + error;
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
        <span className="error-message"></span>
      </form>
    </div>
  );
}

import { useState, useEffect } from "react";
import { getAuth } from "../utils/auth";
import User from "../components/user";

export default function UserPage() {
  const [users, setUsers] = useState([]);
  const auth = getAuth();

  useEffect(() => {
    fetch("http://localhost:8000/users/", {
      headers: {
        Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setUsers(data))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);

  return (
    <div className="task-container">
      <h1>Users</h1>
      <div class="task-list">
        {users.map((user) => (
          <User user={user} />
        ))}
      </div>
    </div>
  );
}

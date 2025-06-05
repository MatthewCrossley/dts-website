import { useState, useEffect } from "react";
import { getAuth } from "../utils/auth";
import Task from "../components/task";
import "../styles/task.css";

export default function HomePage() {
  const [tasks, setTasks] = useState([]);
  const auth = getAuth();

  useEffect(() => {
    fetch("http://localhost:8000/tasks/", {
      headers: {
        Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setTasks(data))
      .catch((error) => console.error("Error fetching tasks:", error));
  }, []);

  return (
    <div className="task-container">
      <h1>Your Tasks</h1>
      <div className="task-list">
        {tasks.map((task) => (
          <Task task={task} />
        ))}
      </div>
    </div>
  );
}

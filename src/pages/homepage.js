import { useState, useEffect } from "react";
import { getAuth } from "../utils/auth";
import Task from "../components/task";
import "../styles/task.css";

export default function HomePage() {
  const [tasks, setTasks] = useState([]);
  const auth = getAuth();

  useEffect(() => {
    fetch("https://human-canidae-matthewcrossley-75876ff3.koyeb.app/tasks/", {
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
        {Array.isArray(tasks) && tasks.map((task) => <Task task={task} />)}
      </div>
    </div>
  );
}

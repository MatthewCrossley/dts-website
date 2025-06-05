import { useEffect, useState } from "react";
import { getAuth } from "../utils/auth";

import { useNavigate, useParams } from "react-router-dom";
import "../styles/task.css";

export default function TaskPage() {
  const { taskId } = useParams();
  const [task, setTask] = useState({});
  const [users, setUsers] = useState([]);
  const [creator, setCreator] = useState(null);
  const auth = getAuth();
  const navigate = useNavigate();

  useEffect(() => {
    let request;
    if (!taskId || taskId.length === 0) {
      request = new Promise((resolve) => {
        resolve({
          title: "",
          description: "",
          completed: false,
          due: null,
          assigned_to: null,
          created_by: auth.id,
          created_at: new Date().toString(),
        });
      });
    } else {
      request = fetch(`http://localhost:8000/tasks/${taskId}`, {
        headers: {
          Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
        },
      }).then((response) => response.json());
    }

    request
      .then((data) => {
        setTask(data);
        return data;
      })
      .catch((error) => console.error("Error fetching task:", error))
      .then((task) => {
        fetch("http://localhost:8000/users/", {
          headers: {
            Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            setUsers(data);
            setCreator(data.find((user) => user.id === task.created_by));
          })
          .catch((error) => console.error("Error fetching users:", error));
      });
  }, [taskId]);

  function handleSubmit(e) {
    e.preventDefault();

    let request;
    if (e.nativeEvent.submitter.id === "delete") {
      if (!window.confirm("Are you sure you want to delete this task?")) {
        return;
      }
      request = fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
        },
      }).then(async (response) => {
        if (response.ok) {
          navigate("/");
        } else {
          let error = (await response.json()).detail;
          let errorMessage = "";
          if (Array.isArray(error)) {
            error = error[0];
          }
          if (typeof error === "string") {
            errorMessage = error;
          } else {
            errorMessage = error.loc.join(".") + ": " + error.msg;
          }
          document.querySelector(".error-message").textContent = errorMessage;
        }
      });
    } else {
      if (!taskId || taskId.length === 0) {
        request = fetch("http://localhost:8000/tasks/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
          },
          body: JSON.stringify(task),
        });
      } else {
        request = fetch(`http://localhost:8000/tasks/${taskId}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
          },
          body: JSON.stringify(task),
        });
      }
      request = request.then(async (response) => {
        if (!response.ok) {
          let error = (await response.json()).detail;
          let errorMessage = "";
          if (Array.isArray(error)) {
            error = error[0];
          }
          if (typeof error === "string") {
            errorMessage = error;
          } else {
            errorMessage = error.loc.join(".") + ": " + error.msg;
          }
          document.querySelector(".error-message").textContent = errorMessage;
          return;
        }

        if (!taskId || taskId.length === 0) {
          navigate(`/task/${await response.json()}`);
        } else {
          setTask(await response.json());
        }
      });
    }

    return request.catch((error) => {
      document.querySelector(".error-message").textContent = error;
    });
  }

  return (
    <div className="task-container">
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title:</label>
          <input
            type="text"
            id="title"
            value={task.title || ""}
            onChange={(e) => setTask({ ...task, title: e.target.value })}
          />
        </div>
        <span>
          Created {new Date(task.created_at).toLocaleString()}{" "}
          {creator && `by ${creator.username}`}
        </span>

        <div>
          <label htmlFor="completed">Completed:</label>
          <input
            type="checkbox"
            id="completed"
            checked={task.completed || false}
            onChange={(e) => setTask({ ...task, completed: e.target.checked })}
          />
        </div>

        <div>
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={task.description || ""}
            onChange={(e) => setTask({ ...task, description: e.target.value })}
          />
        </div>

        <div>
          <label htmlFor="due">Due:</label>
          <input
            type="datetime-local"
            id="due"
            value={
              task.due ? new Date(task.due).toISOString().slice(0, 16) : ""
            }
            onChange={(e) =>
              setTask({ ...task, due: new Date(e.target.value) })
            }
          />
        </div>

        <div>
          <label htmlFor="assigned_to">Assigned To:</label>
          <select
            id="assigned_to"
            value={task.assigned_to || ""}
            onChange={(e) => {
              if (e.target.value && e.target.value.length > 0) {
                setTask({ ...task, assigned_to: e.target.value });
              } else {
                setTask({ ...task, assigned_to: null });
              }
            }}
          >
            <option value="">Unassigned</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Save Changes</button>
        <br />
        {taskId && taskId.length > 0 ? (
          <button type="submit" id="delete">
            Delete task
          </button>
        ) : null}
        <div className="error-message"></div>
      </form>
    </div>
  );
}

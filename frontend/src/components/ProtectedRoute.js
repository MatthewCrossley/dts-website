import { Navigate, useLocation } from "react-router-dom";
import { getAuth, setAuth } from "../utils/auth";

export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const auth = getAuth();

  if (auth) {
    fetch("http://localhost:8000/users/current", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${btoa(`${auth.username}:${auth.password}`)}`,
      },
    }).then((response) => {
      if (!response.ok) {
        // If the response is not ok, clear auth and redirect to login
        setAuth(null);
        alert("Unauthorized. Please log in again.");
        return <Navigate to="/login" state={{ from: location }} replace />;
      }
    });
  }

  // If not authenticated and not already on login page, redirect to login
  if (!auth && location.pathname !== "/login") {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated and on login page, redirect to home
  if (auth && location.pathname === "/login") {
    return <Navigate to="/" replace />;
  }

  return children;
}

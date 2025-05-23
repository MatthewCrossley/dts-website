import { Route, Routes } from "react-router-dom";
import "./app.css";
import ProtectedRoute from "./components/ProtectedRoute";
import NavBar from "./components/navbar";
import HomePage from "./pages/homepage";
import LoginPage from "./pages/login";
import TaskPage from "./pages/task";

export default function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/task/:taskId"
          element={
            <ProtectedRoute>
              <TaskPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

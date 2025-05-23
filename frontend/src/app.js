import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/homepage";
import LoginPage from "./pages/login";
import ProtectedRoute from "./components/ProtectedRoute";
import NavBar from "./components/navbar";

export default function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={
          <ProtectedRoute>
            <HomePage />
          </ProtectedRoute>
        } />
      </Routes>
    </>
  );
}

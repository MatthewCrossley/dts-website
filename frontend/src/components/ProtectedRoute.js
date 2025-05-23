import { Navigate, useLocation } from 'react-router-dom';
import { getAuth } from '../utils/auth';

export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const auth = getAuth();

  // If not authenticated and not already on login page, redirect to login
  if (!auth && location.pathname !== '/login') {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated and on login page, redirect to home
  if (auth && location.pathname === '/login') {
    return <Navigate to="/" replace />;
  }

  return children;
}

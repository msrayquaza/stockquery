// src/App.js
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import { getUsuarioInfo } from './api/auth';
import UsuariosPage from './pages/UsuariosPage'; 

function App() {
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const verificarSesion = async () => {
      try {
        const data = await getUsuarioInfo();
        localStorage.setItem('user', JSON.stringify(data));
        setIsAuthenticated(true);
      } catch (error) {
        console.warn('No autenticado');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    verificarSesion();
  }, []);

  if (loading) {
    return <div>Cargando...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/usuarios"
          element={isAuthenticated ? <UsuariosPage /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;

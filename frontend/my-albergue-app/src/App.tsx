import React, { useEffect, useState } from 'react';
import { createTheme, MantineProvider, rem } from '@mantine/core';  // Importar MantineProvider
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { AdminPage } from './pages/AdminPage';
import { VolunteerPage } from './pages/VolunteerPage';
import { AdoptantePage } from './pages/AdoptantePage';
import 'normalize.css';
import { AlbergueAPIClient } from './services/Albergue';

const theme = createTheme({
  colors: {
    deepBlue: [
      '#eef3ff',
      '#dce4f5',
      '#b9c7e2',
      '#94a8d0',
      '#748dc1',
      '#5f7cb8',
      '#5474b4',
      '#44639f',
      '#39588f',
      '#2d4b81',
    ],
    blue: [
      '#eef3ff',
      '#dee2f2',
      '#bdc2de',
      '#98a0ca',
      '#7a84ba',
      '#6672b0',
      '#5c68ac',
      '#4c5897',
      '#424e88',
      '#364379',
    ],
  },

  shadows: {
    md: '1px 1px 3px rgba(0, 0, 0, .25)',
    xl: '5px 5px 3px rgba(0, 0, 0, .25)',
  },

  headings: {
    fontFamily: 'Roboto, sans-serif',
    sizes: {
      h1: { fontSize: rem(36) },
    },
  },
});

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  // Verificar la autenticación llamando al backend
  useEffect(() => {
    const checkAuth = async () => {
      // Usar AlbergueAPIClient para hacer la solicitud al backend
      AlbergueAPIClient.get(
        '/check-auth/',
        null,
        (response) => {
          setIsAuthenticated(true);
        },
        (error) => {
          setIsAuthenticated(false);
        }
      );
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return <p>Verificando autenticación...</p>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <MantineProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <PrivateRoute>
                <AdminPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/volunteer"
            element={
              <PrivateRoute>
                <VolunteerPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/adoptante"
            element={
              <PrivateRoute>
                <AdoptantePage />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </MantineProvider>
  );
}

export default App;

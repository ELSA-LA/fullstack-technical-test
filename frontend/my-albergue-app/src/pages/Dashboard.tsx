import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const checkUserRole = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/get-role/', {
            headers: { Authorization: `Bearer ${token}` },
          });
          
          // Redirigir basado en el rol del usuario
          const role = response.data;
          if (role === 'admin') {
            navigate('/admin');
          } else if (role === 'voluntario') {
            navigate('/volunteer');
          } else if (role === 'adoptante') {
            navigate('/adoptante');
          }
        } catch (error) {
          console.error("Error fetching role", error);
          navigate('/login');
        }
      } else {
        navigate('/login');
      }
    };
    checkUserRole();
  }, [navigate]);

  return (
    <div>
      <h1>Redirigiendo...</h1>
    </div>
  );
};

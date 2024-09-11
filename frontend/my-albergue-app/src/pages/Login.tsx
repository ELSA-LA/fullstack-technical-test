import React, { useState } from 'react';
import { TextInput, Button, Container, Title, Notification } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import { AlbergueAPIClient } from '../services/Albergue';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    AlbergueAPIClient.post('/token/', { email, password }, (response) => {
        const role = response.data.role;

        if (role === 'S') {
            navigate('/admin');
        } else if (role === 'V') {
            navigate('/volunteer');
        } else if (role === 'A') {
            navigate('/adoptante');
        }
    }).catch(() => {
        setError('Invalid credentials');
    });
  }

  return (
    <Container>
      <Title>Login</Title>
      {error && <Notification color="red">{error}</Notification>}
      <TextInput
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.currentTarget.value)}
        placeholder="Enter your email"
      />
      <TextInput
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.currentTarget.value)}
        placeholder="Enter your password"
      />
      <Button onClick={handleLogin} fullWidth>Login</Button>
    </Container>
  );
};

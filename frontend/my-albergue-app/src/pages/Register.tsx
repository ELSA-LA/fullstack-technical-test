import React, { useState } from 'react';
import { TextInput, Button, Select, Container, Title, Notification } from '@mantine/core';
import axios from 'axios';

export const Register = () => {
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rol, setRol] = useState('V');
  const [error, setError] = useState('');

  const handleRegister = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/api/registro/', { nombre, apellido, email, password, rol });
      window.location.href = '/login'; // Redirigir al login
    } catch (error) {
      setError('Error registering user');
    }
  };

  return (
    <Container>
      <Title>Register</Title>
      {error && <Notification color="red">{error}</Notification>}
      <TextInput
        label="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.currentTarget.value)}
        placeholder="Enter your name"
      />
      <TextInput
        label="Apellido"
        value={apellido}
        onChange={(e) => setApellido(e.currentTarget.value)}
        placeholder="Enter your last name"
      />
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
      <Select
        label="Rol"
        value={rol}
        onChange={(value) => setRol(value ?? 'V')} 
        data={[
          { value: 'V', label: 'Voluntario' },
          { value: 'A', label: 'Adoptante' },
        ]}
      />
      <Button onClick={handleRegister}>Register</Button>
    </Container>
  );
};

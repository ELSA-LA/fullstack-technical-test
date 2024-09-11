import React from 'react';
import { Container, Title, Tabs, Button } from '@mantine/core';
import { ManageAnimals } from './ManageAnimals';
import { ManageAdopciones } from './ManageAdopciones';
import { ManageUsuarios } from './ManageUsuarios';
import { useNavigate } from 'react-router-dom';
import { AlbergueAPIClient } from '../services/Albergue';

export const AdminPage = () => {
    const navigate = useNavigate();
    const handleLogout = () => {
        AlbergueAPIClient.removeUser();  // Remover el token del localStorage
        navigate('/login');  // Redirigir a la página de login
    };
    console.log("En admin");
  return (
    <Container>
      <Title>Panel de Administrador</Title>
      <Tabs>
        <Tabs.List>
          <Tabs.Tab value="animales">Animales</Tabs.Tab>
          <Tabs.Tab value="adopciones">Adopciones</Tabs.Tab>
          <Tabs.Tab value="usuarios">Usuarios</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="animales">
          <ManageAnimals />
        </Tabs.Panel>

        <Tabs.Panel value="adopciones">
          <ManageAdopciones />
        </Tabs.Panel>

        <Tabs.Panel value="usuarios">
          <ManageUsuarios />
        </Tabs.Panel>
      </Tabs>
      <Button onClick={handleLogout} color="red" style={{ marginTop: '1rem' }}>
        Logout
      </Button>
    </Container>
  );
};

import React, { useEffect, useState } from 'react';
import { Container, Title, Card, Text, Button, Select, Notification, Pagination } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { AlbergueAPIClient } from '../services/Albergue';

interface Animal {
  id: number;
  nombre: string;
  edad: number;
  raza: string;
  estado: string;
}

interface Adopcion {
  id: number;
  animal: string;
  adoptador: string;
  estado: string;
}

interface Adoptante {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
}

export const VolunteerPage = () => {
  const navigate = useNavigate();

  // Estados locales
  const [animales, setAnimales] = useState<Animal[]>([]);
  const [adopciones, setAdopciones] = useState<Adopcion[]>([]);
  const [adoptantes, setAdoptantes] = useState<Adoptante[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedAnimalId, setSelectedAnimalId] = useState<number | null>(null);
  const [selectedEstado, setSelectedEstado] = useState<string>('EA');

  // Paginación para Animales
  const [animalPage, setAnimalPage] = useState(1);
  const [totalAnimalPages, setTotalAnimalPages] = useState(1);

  // Paginación para Adopciones
  const [adopcionPage, setAdopcionPage] = useState(1);
  const [totalAdopcionPages, setTotalAdopcionPages] = useState(1);

  // Paginación para Adoptantes
  const [adoptantePage, setAdoptantePage] = useState(1);
  const [totalAdoptantePages, setTotalAdoptantePages] = useState(1);

  const handleLogout = () => {
    AlbergueAPIClient.removeUser();
    navigate('/login');
  };

  const fetchAnimales = async (page = 1) => {
    AlbergueAPIClient.get(`/animales/?page=${page}`, null, (response) => {
      setAnimales(response.data.results);
      setTotalAnimalPages(response.data.total_pages);
      setLoading(false);
    }, (error) => {
      setError('Error al cargar los animales.');
    });
  };

  const fetchAdopciones = async (page = 1) => {
    AlbergueAPIClient.get(`/adopciones/?page=${page}`, null, (response) => {
      setAdopciones(response.data.results);
      setTotalAdopcionPages(response.data.total_pages);
    });
  };

  const fetchAdoptantes = async (page = 1) => {
    AlbergueAPIClient.get(`/usuarios/?rol=A&page=${page}`, null, (response) => {
      setAdoptantes(response.data.results);
      setTotalAdoptantePages(response.data.total_pages);
    });
  };

  const handleUpdateEstado = async (animalId: number) => {
    AlbergueAPIClient.patch(`/animales/${animalId}/`, { estado: selectedEstado }, () => {
      setSuccess(`El estado del animal con ID ${animalId} ha sido actualizado.`);
      fetchAnimales(animalPage);
    }, (error) => {
      setError('Error al actualizar el estado del animal.');
    });
  };

  const getAnimalNombre = (animalId: string) => {
    const animal = animales.find((animal) => animal.id.toString() === animalId);
    return animal ? animal.nombre : 'Desconocido';
  };

  const getAdoptadorNombre = (adoptadorId: string) => {
    const adoptante = adoptantes.find((adoptante) => adoptante.id.toString() === adoptadorId);
    return adoptante ? `${adoptante.nombre} ${adoptante.apellido}` : 'Desconocido';
  };

  useEffect(() => {
    fetchAnimales(animalPage);
    fetchAdopciones(adopcionPage);
    fetchAdoptantes(adoptantePage);
  }, [animalPage, adopcionPage, adoptantePage]);

  if (loading) {
    return <Text>Cargando información...</Text>;
  }

  return (
    <Container>
      <Title>Gestión de Animales, Adopciones y Adoptantes (Voluntario)</Title>

      {error && <Notification color="red" onClose={() => setError('')}>{error}</Notification>}
      {success && <Notification color="green" onClose={() => setSuccess('')}>{success}</Notification>}

      {/* Sección de Animales */}
      <Title order={2}>Animales</Title>
      {animales.map((animal) => (
        <Card key={animal.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Nombre: {animal.nombre}</Text>
          <Text>Edad: {animal.edad}</Text>
          <Text>Raza: {animal.raza}</Text>
          <Text>Estado: {animal.estado === 'EA' ? 'En adopción' : 'Adoptado'}</Text>

          <Select
            label="Cambiar Estado"
            value={selectedAnimalId === animal.id ? selectedEstado : ''}
            onChange={(value) => {
              setSelectedAnimalId(animal.id);
              setSelectedEstado(value || 'EA');
            }}
            data={[
              { value: 'EA', label: 'En adopción' },
              { value: 'AD', label: 'Adoptado' },
            ]}
          />
          <Button
            onClick={() => handleUpdateEstado(animal.id)}
            disabled={selectedAnimalId !== animal.id}
            color="blue"
            style={{ marginTop: '10px' }}
          >
            Actualizar Estado
          </Button>
        </Card>
      ))}

      <Pagination
        value={animalPage}
        onChange={setAnimalPage}
        total={totalAnimalPages}
        withEdges
        style={{ marginTop: '1rem' }}
        disabled={totalAnimalPages <= 1}
      />

      {/* Sección de Adopciones */}
      <Title order={2}>Adopciones</Title>
      {adopciones.map((adopcion) => (
        <Card key={adopcion.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Animal: {getAnimalNombre(adopcion.animal)}</Text>
          <Text>Adoptador: {getAdoptadorNombre(adopcion.adoptador)}</Text>
          <Text>Estado: {adopcion.estado === 'P' ? 'En proceso' : 'Finalizado'}</Text>
        </Card>
      ))}

      <Pagination
        value={adopcionPage}
        onChange={setAdopcionPage}
        total={totalAdopcionPages}
        withEdges
        style={{ marginTop: '1rem' }}
        disabled={totalAdopcionPages <= 1}
      />

      {/* Sección de Adoptantes */}
      <Title order={2}>Adoptantes</Title>
      {adoptantes.map((adoptante) => (
        <Card key={adoptante.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Nombre: {adoptante.nombre} {adoptante.apellido}</Text>
          <Text>Email: {adoptante.email}</Text>
        </Card>
      ))}

      <Pagination
        value={adoptantePage}
        onChange={setAdoptantePage}
        total={totalAdoptantePages}
        withEdges
        style={{ marginTop: '1rem' }}
        disabled={totalAdoptantePages <= 1}
      />

      <Button onClick={handleLogout} color="red" style={{ marginTop: '1rem' }}>
        Logout
      </Button>
    </Container>
  );
};
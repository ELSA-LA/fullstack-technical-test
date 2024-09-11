import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Title, Card, Button, Text, Notification, Pagination } from '@mantine/core';
import { AlbergueAPIClient } from '../services/Albergue';

const estadoMap: Record<string, string> = {
    'EA': 'En adopción',
    'AD': 'Adoptado',
    'EE': 'En espera de adopción',
};

interface Animal {
  id: number;
  nombre: string;
  raza: string;
  estado: string;
  tipo: string;
}

interface Adopcion {
  id: number;
  animal: string;
  estado: string;
}

export const AdoptantePage = () => {
  const [animales, setAnimales] = useState<Animal[]>([]);
  const [adopciones, setAdopciones] = useState<Adopcion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState<boolean>(false);
  const [hasPrevious, setHasPrevious] = useState<boolean>(false); 

  const navigate = useNavigate();

  // Función para hacer logout
  const handleLogout = () => {
    AlbergueAPIClient.removeUser();
    navigate('/login');
  };

  // Obtener los animales disponibles para adopción
  const fetchAnimales = async (page = 1) => {
    AlbergueAPIClient.get(`/animales/?page=${page}`, null, (response) => {
      setAnimales(response.data.results);  // results contiene los datos de la página actual
      setTotalPages(response.data.total_pages);  // total_pages depende del backend
      setLoading(false);
      setHasNext(response.data.next !== null);
      setHasPrevious(response.data.previous !== null);
    },(error) => {
        setError('Error al cargar los animales.');
    });
  };

  // Obtener las adopciones del adoptante
  const fetchAdopciones = async (page = 1) => {
    const animalIds = animales.map((animal) => animal.id).join(',');
    AlbergueAPIClient.get(`/adopciones/?page=${page}&estado=P&animal_ids=${animalIds}`, null, (response) => {
      setAdopciones(response.data.results);
    },(error) => {
        setError('Error al cargar las adopciones.');
    });
  };

  const solicitarAdopcion = async (animalId: number) => {
    if (tieneAdopcionEnProceso(animalId)) {
      setError('Ya tienes una adopción en proceso para este animal.');
      return;
    }

    AlbergueAPIClient.post('/adopciones/', { animal: animalId }, (response) => {
      setSuccess(`Solicitud de adopción para el animal con ID ${animalId} enviada.`);
      fetchAdopciones();  // Actualizar las adopciones
    });
  };

  // Verificar si ya tiene una adopción en proceso para este animal
  const tieneAdopcionEnProceso = (animalId: number) => {
    if (!Array.isArray(adopciones)) {
        return false;  // Asegurarse de que adopciones es un array antes de usar .some()
    }
    return adopciones.some((adopcion) => {
        return Number(adopcion.animal) === animalId && adopcion.estado === 'P';
    });
  };

  useEffect(() => {
    fetchAnimales(currentPage);
  }, [currentPage]);

  useEffect(() => {
    if (animales.length > 0) {
      fetchAdopciones();
    }
  }, [animales]);

  const handlePageChange = (page: number) => {
    if ((page > 0 && hasNext) || (page < currentPage && hasPrevious)) {
      setCurrentPage(page);  // Cambiar la página actual solo si hay next/previous
    }
  };


  if (loading) {
    return <Text>Cargando animales...</Text>;
  }

  if (error) {
    return <Text color="red">{error}</Text>;
  }

  return (
    <Container>
      <Title>Animales Disponibles para Adopción</Title>
      {success && <Notification color="green">{success}</Notification>}
      {animales.length > 0 ? (
        animales.map((animal) => (
          <Card key={animal.id} shadow="sm" padding="lg" style={{ marginBottom: '1rem' }}>
            <Text>Nombre: {animal.nombre}</Text>
            <Text>Raza: {animal.raza}</Text>
            <Text>Estado: {estadoMap[animal.estado] || 'Desconocido'}</Text>
            <Text>Tipo: {animal.tipo === 'P' ? 'Perro' : 'Gato'}</Text>
            <Button
              onClick={() => solicitarAdopcion(animal.id)}
              disabled={tieneAdopcionEnProceso(animal.id)}  // Desactivar si ya hay adopción en proceso
            >
              {tieneAdopcionEnProceso(animal.id) ? 'Adopción en Proceso' : 'Solicitar Adopción'}
            </Button>
          </Card>
        ))
      ) : (
        <Text>No hay animales disponibles para adopción.</Text>
      )}
      <Pagination
        value={currentPage}
        onChange={handlePageChange}
        total={totalPages}
        style={{ marginTop: '1rem' }}
        withEdges
        disabled={totalPages <= 1} 
      />
      <Button onClick={handleLogout} color="red" style={{ marginTop: '1rem' }}>
        Logout
      </Button>
    </Container>
  );
};
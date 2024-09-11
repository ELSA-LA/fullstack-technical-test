import React, { useEffect, useState } from 'react';
import { Container, Title, Button, Card, Text, TextInput, Select, Pagination } from '@mantine/core';
import { AlbergueAPIClient } from '../services/Albergue';

interface Animal {
  id: number;
  nombre: string;
  edad: number;
  raza: string;
  estado: string;
  tipo: string;
}

export const ManageAnimals = () => {
  const [animales, setAnimales] = useState<Animal[]>([]);
  const [loading, setLoading] = useState(true);
  const [nombre, setNombre] = useState('');
  const [edad, setEdad] = useState<number | null>(null);
  const [raza, setRaza] = useState('');
  const [tipo, setTipo] = useState('P'); // 'P' para perro, 'G' para gato
  const [estado, setEstado] = useState('EA'); // 'EA' para "En adopción"
  const [editingId, setEditingId] = useState<number | null>(null);

  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState<boolean>(false);
  const [hasPrevious, setHasPrevious] = useState<boolean>(false);

  // Obtener la lista de animales con paginación
  const fetchAnimales = async (page = 1) => {
    AlbergueAPIClient.get(`/animales/?page=${page}`, null, (response) => {
      setAnimales(response.data.results);
      setTotalPages(response.data.total_pages);
      setHasNext(response.data.next !== null);
      setHasPrevious(response.data.previous !== null);
      setLoading(false);
    });
  };

  // Crear o actualizar animal
  const handleSubmit = async () => {
    const animal = { nombre, edad, raza, tipo, estado };
    if (editingId) {
      // Actualizar animal
      AlbergueAPIClient.put(`/animales/${editingId}/`, animal, () => {
        fetchAnimales(currentPage);
        resetForm();
      });
    } else {
      // Crear nuevo animal
      AlbergueAPIClient.post('/animales/', animal, () => {
        fetchAnimales(currentPage);
        resetForm();
      });
    }
  };

  // Eliminar animal
  const deleteAnimal = (id: number) => {
    AlbergueAPIClient.post(`/animales/${id}/`, null, () => {
      fetchAnimales(currentPage);
    });
  };

  // Editar un animal
  const editAnimal = (animal: Animal) => {
    setEditingId(animal.id);
    setNombre(animal.nombre);
    setEdad(animal.edad);
    setRaza(animal.raza);
    setTipo(animal.tipo);
    setEstado(animal.estado);
  };

  // Reiniciar el formulario
  const resetForm = () => {
    setEditingId(null);
    setNombre('');
    setEdad(null);
    setRaza('');
    setTipo('P'); // Volver a perro por defecto
    setEstado('EA'); // En adopción por defecto
  };

  useEffect(() => {
    fetchAnimales(currentPage);
  }, [currentPage]);

  const handlePageChange = (page: number) => {
    if ((page > 0 && hasNext) || (page < currentPage && hasPrevious)) {
      setCurrentPage(page);
    }
  };

  if (loading) {
    return <Text>Cargando animales...</Text>;
  }

  return (
    <Container>
      <Title>Gestión de Animales</Title>
      <TextInput
        label="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.currentTarget.value)}
      />
      <TextInput
        label="Edad"
        value={edad || ''}
        type="number"
        onChange={(e) => setEdad(Number(e.currentTarget.value))}
      />
      <TextInput
        label="Raza"
        value={raza}
        onChange={(e) => setRaza(e.currentTarget.value)}
      />
      <Select
        label="Tipo"
        value={tipo}
        onChange={(value) => setTipo(value || 'P')}
        data={[
          { value: 'P', label: 'Perro' },
          { value: 'G', label: 'Gato' },
        ]}
      />
      <Select
        label="Estado"
        value={estado}
        onChange={(value) => setEstado(value || 'EA')}
        data={[
          { value: 'EA', label: 'En adopción' },
          { value: 'AD', label: 'Adoptado' },
          { value: 'EE', label: 'En espera de adopción' },
        ]}
      />
      <Button onClick={handleSubmit}>
        {editingId ? 'Actualizar Animal' : 'Agregar Animal'}
      </Button>
      {editingId && <Button onClick={resetForm} color="gray">Cancelar</Button>}

      {animales.map((animal) => (
        <Card key={animal.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Nombre: {animal.nombre}</Text>
          <Text>Edad: {animal.edad}</Text>
          <Text>Raza: {animal.raza}</Text>
          <Text>Tipo: {animal.tipo === 'P' ? 'Perro' : 'Gato'}</Text>
          <Text>Estado: {estadoMap[animal.estado] || 'Desconocido'}</Text>
          <Button onClick={() => editAnimal(animal)} color="blue" style={{ marginRight: '10px' }}>
            Editar
          </Button>
          <Button onClick={() => deleteAnimal(animal.id)} color="red">
            Eliminar
          </Button>
        </Card>
      ))}

      <Pagination
        value={currentPage}
        onChange={handlePageChange}
        total={totalPages}
        style={{ marginTop: '1rem' }}
        withEdges
        disabled={totalPages <= 1}
      />
    </Container>
  );
};

const estadoMap: Record<string, string> = {
  EA: 'En adopción',
  AD: 'Adoptado',
  EE: 'En espera de adopción',
};
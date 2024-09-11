import React, { useEffect, useState } from 'react';
import { Container, Title, Card, Text, Button, Select, Pagination } from '@mantine/core';
import { AlbergueAPIClient } from '../services/Albergue';

interface Adopcion {
  id: number;
  animal: string;
  adoptador: string;
  voluntario: string;
  estado: string;
}

interface Option {
  value: string;
  label: string;
}

export const ManageAdopciones = () => {
  const [adopciones, setAdopciones] = useState<Adopcion[]>([]);
  const [loading, setLoading] = useState(true);
  const [animal, setAnimal] = useState('');
  const [adoptador, setAdoptador] = useState('');
  const [voluntario, setVoluntario] = useState('');
  const [estado, setEstado] = useState('P');  // Estado por defecto: 'En proceso'
  const [editingId, setEditingId] = useState<number | null>(null);

  const [animalOptions, setAnimalOptions] = useState<Option[]>([]);
  const [adoptadorOptions, setAdoptadorOptions] = useState<Option[]>([]);
  const [voluntarioOptions, setVoluntarioOptions] = useState<Option[]>([]);

  // Para la paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState<boolean>(false);
  const [hasPrevious, setHasPrevious] = useState<boolean>(false);

  const fetchAdopciones = async (page = 1) => {
    AlbergueAPIClient.get(`/adopciones/?page=${page}`, null, (response) => {
      setAdopciones(response.data.results);
      setTotalPages(response.data.total_pages);
      setHasNext(response.data.next !== null);
      setHasPrevious(response.data.previous !== null);
      setLoading(false);
    });
  };

  const fetchAnimales = async () => {
    const animalIds = adopciones.map((adopcion) => adopcion.animal).join(',');
    AlbergueAPIClient.get(`/animales/?animal_ids=${animalIds}`, null, (response) => {
      const options = response.data.results.map((animal: any) => ({
        value: animal.id.toString(),
        label: animal.nombre,
      }));
      setAnimalOptions(options);
    });
  };

  const fetchAdoptadores = async () => {
    const adoptadoresIds = adopciones.map((adopcion) => adopcion.adoptador).join(',');
    AlbergueAPIClient.get(`/usuarios/?user_ids=${adoptadoresIds}`, { rol: 'A' }, (response) => {
      const options = response.data.results.map((adoptador: any) => ({
        value: adoptador.id.toString(),
        label: `${adoptador.nombre} ${adoptador.apellido}`,
      }));
      setAdoptadorOptions(options);
    });
  };

  const fetchVoluntarios = async () => {
    const voluntariosIds = adopciones.map((adopcion) => adopcion.voluntario).join(',');
    AlbergueAPIClient.get(`/usuarios/?user_ids=${voluntariosIds}`, { rol: 'V' }, (response) => {
      const options = response.data.results.map((voluntario: any) => ({
        value: voluntario.id.toString(),
        label: `${voluntario.nombre} ${voluntario.apellido}`,
      }));
      setVoluntarioOptions(options);
    });
  };

  useEffect(() => {
    fetchAdopciones(currentPage);
    fetchAnimales();
    fetchAdoptadores();
    fetchVoluntarios();
  }, [currentPage]);

  useEffect(() => {
    fetchAnimales();
    fetchAdoptadores();
    fetchVoluntarios();
  }, [adopciones]);

  // Obtener el nombre del animal a partir de su ID
  const getAnimalNombre = (animalId: string) => {
    animalId = String(animalId);
    const animal = animalOptions.find((option) => option.value === animalId);
    return animal ? animal.label : 'Desconocido';
  };

  // Obtener el nombre del adoptador a partir de su ID
  const getAdoptadorNombre = (adoptadorId: string) => {
    adoptadorId = String(adoptadorId);
    const adoptador = adoptadorOptions.find((option) => option.value === adoptadorId);
    return adoptador ? adoptador.label : 'Desconocido';
  };

  const getVoluntarioNombre = (voluntarioId: string) => {
    voluntarioId = String(voluntarioId);
    const voluntario = voluntarioOptions.find((option) => option.value === voluntarioId);
    return voluntario ? voluntario.label : 'Desconocido';
  };

  // Crear o actualizar adopción
  const handleSubmit = async () => {
    const adopcion = { animal, adoptador, voluntario, estado };
    if (editingId) {
      AlbergueAPIClient.put(`/adopciones/${editingId}/`, adopcion, () => {
        fetchAdopciones(currentPage);
        resetForm();
      });
    } else {
      AlbergueAPIClient.post('/adopciones/', adopcion, () => {
        fetchAdopciones(currentPage);
        resetForm();
      });
    }
  };

  // Eliminar adopción
  const deleteAdopcion = (id: number) => {
    AlbergueAPIClient.post(`/adopciones/${id}/`, null, () => {
      fetchAdopciones(currentPage);
    });
  };

  // Cargar datos en el formulario para editar
  const editAdopcion = (adopcion: Adopcion) => {
    setEditingId(adopcion.id);
    setAnimal(adopcion.animal);
    setAdoptador(adopcion.adoptador);
    setVoluntario(adopcion.voluntario);
    setEstado(adopcion.estado);
  };

  // Restablecer formulario
  const resetForm = () => {
    setEditingId(null);
    setAnimal('');
    setAdoptador('');
    setVoluntario('');
    setEstado('P');  // Estado por defecto: 'En proceso'
  };

  const handlePageChange = (page: number) => {
    if ((page > 0 && hasNext) || (page < currentPage && hasPrevious)) {
      setCurrentPage(page);
    }
  };

  if (loading) {
    return <Text>Cargando adopciones...</Text>;
  }

  return (
    <Container>
      <Title>Gestión de Adopciones</Title>

      <Select
        label="Animal"
        value={animal}
        onChange={(value) => setAnimal(value || '')}
        placeholder="Seleccionar animal"
        data={animalOptions}  // Datos dinámicos de animales
      />
      <Select
        label="Adoptador"
        value={adoptador}
        onChange={(value) => setAdoptador(value || '')}
        placeholder="Seleccionar adoptador"
        data={adoptadorOptions}  // Datos dinámicos de adoptadores
      />
      <Select
        label="Voluntario"
        value={voluntario}
        onChange={(value) => setVoluntario(value || '')}
        placeholder="Seleccionar voluntario"
        data={voluntarioOptions}  // Datos dinámicos de voluntarios
      />
      <Select
        label="Estado"
        value={estado}
        onChange={(value) => setEstado(value || 'P')}
        data={[
          { value: 'P', label: 'En proceso' },
          { value: 'F', label: 'Finalizado' },
        ]}
      />

      <Button onClick={handleSubmit}>
        {editingId ? 'Actualizar Adopción' : 'Agregar Adopción'}
      </Button>
      {editingId && <Button onClick={resetForm} color="gray">Cancelar</Button>}

      {adopciones.map((adopcion) => (
        <Card key={adopcion.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Animal: {getAnimalNombre(adopcion.animal)}</Text>
          <Text>Adoptador: {getAdoptadorNombre(adopcion.adoptador)}</Text>
          <Text>Voluntario: {getVoluntarioNombre(adopcion.voluntario)}</Text>
          <Text>Estado: {adopcion.estado === 'P' ? 'En proceso' : 'Finalizado'}</Text>
          <Button onClick={() => editAdopcion(adopcion)} color="blue" style={{ marginRight: '10px' }}>
            Editar
          </Button>
          <Button onClick={() => deleteAdopcion(adopcion.id)} color="red">
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

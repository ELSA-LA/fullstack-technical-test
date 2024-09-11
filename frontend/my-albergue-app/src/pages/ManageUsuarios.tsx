import React, { useEffect, useState } from 'react';
import { Container, Title, Card, Text, Button, TextInput, Select, Pagination } from '@mantine/core';
import { AlbergueAPIClient } from '../services/Albergue';

interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  rol: string;
  password?: string;  // Campo opcional para editar la contraseña
}

export const ManageUsuarios = () => {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [rol, setRol] = useState('V'); // Default rol es voluntario
  const [password, setPassword] = useState('');  // Contraseña para creación o edición
  const [editingId, setEditingId] = useState<number | null>(null);
  
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState<boolean>(false);  // Controlar si hay siguiente página
  const [hasPrevious, setHasPrevious] = useState<boolean>(false);  // Controlar si hay página anterior

  // Fetch usuarios desde la API
  const fetchUsuarios = async (page = 1) => {
    AlbergueAPIClient.get(`/usuarios/?page=${page}`, null, (response) => {
      setUsuarios(response.data.results);  // Cargar usuarios de la página actual
      setTotalPages(response.data.total_pages);  // Total de páginas
      setHasNext(response.data.next !== null);  // Si hay una página siguiente
      setHasPrevious(response.data.previous !== null);  // Si hay una página anterior
      setLoading(false);
    });
  };

  // Crear o actualizar usuario
  const handleSubmit = async () => {
    const user = { nombre, apellido, email, rol, password: password ? password : undefined };
    if (editingId) {
      // Actualizar usuario existente (opcionalmente puede incluir la contraseña)
      AlbergueAPIClient.patch(`/usuarios/${editingId}/`, user, () => {
        fetchUsuarios(currentPage);
        resetForm();
      });
    } else {
      // Crear nuevo usuario
      AlbergueAPIClient.post('/usuarios/', user, () => {
        fetchUsuarios(currentPage);
        resetForm();
      });
    }
  };

  // Eliminar usuario
  const deleteUsuario = (id: number) => {
    AlbergueAPIClient.post(`/usuarios/${id}/`, null, () => {
      fetchUsuarios(currentPage);
    });
  };

  // Cargar datos en el formulario para editar
  const editUsuario = (usuario: Usuario) => {
    setEditingId(usuario.id);
    setNombre(usuario.nombre);
    setApellido(usuario.apellido);
    setEmail(usuario.email);
    setRol(usuario.rol);
  };

  // Reiniciar formulario
  const resetForm = () => {
    setEditingId(null);
    setNombre('');
    setApellido('');
    setEmail('');
    setPassword('');  // Limpiar la contraseña
    setRol('V'); // Default a voluntario
  };

  useEffect(() => {
    fetchUsuarios(currentPage);
  }, [currentPage]);

  const handlePageChange = (page: number) => {
    if ((page > 0 && hasNext) || (page < currentPage && hasPrevious)) {
      setCurrentPage(page);  // Cambiar la página actual solo si hay siguiente/anterior
    }
  };

  if (loading) {
    return <Text>Cargando usuarios...</Text>;
  }

  return (
    <Container>
      <Title>Gestión de Voluntarios y Adoptantes</Title>

      <TextInput label="Nombre" value={nombre} onChange={(e) => setNombre(e.currentTarget.value)} />
      <TextInput label="Apellido" value={apellido} onChange={(e) => setApellido(e.currentTarget.value)} />
      <TextInput label="Email" value={email} onChange={(e) => setEmail(e.currentTarget.value)} />
      <TextInput
        label="Contraseña"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.currentTarget.value)}
        placeholder={editingId ? "Dejar en blanco para no cambiar" : "Ingresar contraseña"}
      />
      <Select
        label="Rol"
        value={rol}
        onChange={(value) => setRol(value ?? 'voluntario')} 
        data={[
          { value: 'V', label: 'Voluntario' },
          { value: 'A', label: 'Adoptante' },
        ]}
      />
      <Button onClick={handleSubmit}>
        {editingId ? 'Actualizar Usuario' : 'Agregar Usuario'}
      </Button>
      {editingId && <Button onClick={resetForm} color="gray">Cancelar</Button>}

      {usuarios.map((usuario) => (
        <Card key={usuario.id} shadow="sm" padding="lg" style={{ marginTop: '1rem' }}>
          <Text>Nombre: {usuario.nombre} {usuario.apellido}</Text>
          <Text>Email: {usuario.email}</Text>
          <Text>Rol: {usuario.rol === 'V' ? 'Voluntario' : 'Adoptante'}</Text>
          <Button onClick={() => editUsuario(usuario)} color="blue" style={{ marginRight: '10px' }}>
            Editar
          </Button>
          <Button onClick={() => deleteUsuario(usuario.id)} color="red">
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
        disabled={totalPages <= 1}  // Deshabilitar si solo hay una página
      />
    </Container>
  );
};
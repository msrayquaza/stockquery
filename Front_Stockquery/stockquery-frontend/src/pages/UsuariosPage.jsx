// src/pages/UsuariosPage.jsx
import React, { useEffect, useState } from 'react';
import {
  getUsuarios,
  createUsuario,
  updateUsuario,
  deleteUsuario
} from '../api/usuarios';
import Navbar from '../components/navigation/Navbar';
import Sidebar from '../components/navigation/Sidebar';
import Modal from '../components/Modal';
import '../styles/UsuariosPage.css';

const UsuariosPage = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [newUsuario, setNewUsuario] = useState({
    nombre: '',
    correo: '',
    contraseña: '',
    rol: 'Operador',
    imagen_perfil: null
  });
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  const fetchUsuarios = async () => {
    try {
      const response = await getUsuarios();
      setUsuarios(response.data);
    } catch (error) {
      console.error('Error al obtener usuarios:', error);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const handleOpenCreateModal = () => {
    setShowCreateModal(true);
  };
  const handleCloseCreateModal = () => {
    setShowCreateModal(false);
    setNewUsuario({
      nombre: '',
      correo: '',
      contraseña: '',
      rol: 'Operador',
      imagen_perfil: null
    });
  };

  const handleOpenEditModal = (usuario) => {
    setEditingUsuario({ ...usuario });
    setShowEditModal(true);
  };
  const handleCloseEditModal = () => {
    setShowEditModal(false);
    setEditingUsuario(null);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createUsuario(newUsuario);
      fetchUsuarios();
      handleCloseCreateModal();
    } catch (error) {
      console.error('Error al crear usuario:', error);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      if (!editingUsuario) return;
      await updateUsuario(editingUsuario.id_usuario, editingUsuario);
      fetchUsuarios();
      handleCloseEditModal();
    } catch (error) {
      console.error('Error al actualizar usuario:', error);
    }
  };

  const handleDelete = async (id_usuario) => {
    if (!window.confirm('¿Estás seguro de eliminar este usuario?')) return;
    try {
      await deleteUsuario(id_usuario);
      fetchUsuarios();
    } catch (error) {
      console.error('Error al eliminar usuario:', error);
    }
  };

  return (
    <>
      <Navbar />
      <Sidebar />
      <div id="app">
        <div className="usuarios-container">
          <h1>Gestión de Usuarios</h1>
          <button className="btn-crear" onClick={handleOpenCreateModal}>+ Crear Usuario</button>

          <table className="usuarios-table">
            <thead>
              <tr>
                <th>Foto</th>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((usuario) => (
                <tr key={usuario.id_usuario}>
                  <td>
                    {usuario.imagen_perfil ? (
                      <img
                        src={usuario.imagen_perfil}
                        alt="Perfil"
                        className="foto-perfil"
                      />
                    ) : (
                      'Sin foto'
                    )}
                  </td>
                  <td>{usuario.nombre}</td>
                  <td>{usuario.apellido}</td>
                  <td>{usuario.correo}</td>
                  <td>{usuario.rol}</td>
                  <td>
                    <button className="btn-edit" onClick={() => handleOpenEditModal(usuario)}>Editar</button>
                    <button className="btn-delete" onClick={() => handleDelete(usuario.id_usuario)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {showCreateModal && (
          <Modal title="Crear Usuario" onClose={handleCloseCreateModal}>
            <form onSubmit={handleCreate} className="form-usuario">
              <label>Nombre</label>
              <input
                type="text"
                placeholder="Ingrese nombre completo"
                value={newUsuario.nombre}
                onChange={(e) => setNewUsuario({ ...newUsuario, nombre: e.target.value })}
                required
              />
              <label>Apellido</label>
              <input
                type="text"
                placeholder="Ingrese nombre completo"
                value={newUsuario.apellido}
                onChange={(e) => setNewUsuario({ ...newUsuario, apellido: e.target.value })}
                required
              />
              <label>Correo</label>
              <input
                type="email"
                placeholder="correo@ejemplo.com"
                value={newUsuario.correo}
                onChange={(e) => setNewUsuario({ ...newUsuario, correo: e.target.value })}
                required
              />

              <label>Contraseña</label>
              <input
                type="password"
                placeholder="Ingrese contraseña"
                value={newUsuario.contraseña}
                onChange={(e) => setNewUsuario({ ...newUsuario, contraseña: e.target.value })}
                required
              />

              <label>Rol</label>
              <select
                value={newUsuario.rol}
                onChange={(e) => setNewUsuario({ ...newUsuario, rol: e.target.value })}
              >
                <option value="Administrador">Administrador</option>
                <option value="Recepcion">Recepcion</option>
                <option value="Almacen">Almacen</option>
                <option value="Produccion">Produccion</option>
              </select>

              <label>Foto de Perfil</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setNewUsuario({ ...newUsuario, imagen_perfil: e.target.files[0] })}
              />

              <div className="modal-buttons">
                <button type="submit" className="btn-submit">Crear</button>
                <button type="button" className="btn-cancel" onClick={handleCloseCreateModal}>Cancelar</button>
              </div>
            </form>
          </Modal>
        )}

        {showEditModal && editingUsuario && (
          <Modal title="Editar Usuario" onClose={handleCloseEditModal}>
            <form onSubmit={handleUpdate} className="form-usuario">
              <label>Nombre</label>
              <input
                type="text"
                placeholder="Ingrese nombre completo"
                value={editingUsuario.nombre}
                onChange={(e) => setEditingUsuario({ ...editingUsuario, nombre: e.target.value })}
                required
              />
              <label>Apellido</label>
              <input
                type="text"
                placeholder="Ingrese nombre completo"
                value={editingUsuario.apellido}
                onChange={(e) => setEditingUsuario({ ...editingUsuario, apellido: e.target.value })}
                required
              />
              <label>Correo</label>
              <input
                type="email"
                placeholder="correo@ejemplo.com"
                value={editingUsuario.correo}
                onChange={(e) => setEditingUsuario({ ...editingUsuario, correo: e.target.value })}
                required
              />

              <label>Contraseña</label>
              <input
                type="password"
                placeholder="Ingrese contraseña"
                value={editingUsuario.contraseña}
                onChange={(e) => setEditingUsuario({ ...editingUsuario, contraseña: e.target.value })}
                required
              />

              <label>Rol</label>
              <select
                value={editingUsuario.rol}
                onChange={(e) => setEditingUsuario({ ...editingUsuario, rol: e.target.value })}
              >
                <option value="Administrador">Administrador</option>
                <option value="Recepcion">Recepcion</option>
                <option value="Almacen">Almacen</option>
                <option value="Produccion">Produccion</option>
              </select>

              <label>Foto de Perfil</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setEditingUsuario({ ...editingUsuario, imagen_perfil: e.target.files[0] })}
              />

              <div className="modal-buttons">
                <button type="submit" className="btn-submit">Actualizar</button>
                <button type="button" className="btn-cancel" onClick={handleCloseEditModal}>Cancelar</button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </>
  );
};

export default UsuariosPage;

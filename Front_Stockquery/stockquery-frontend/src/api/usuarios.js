// src/api/usuarios.js
import api from './apiConfig';

export const getUsuarios = () => {
  return api.get('/usuarios/');
};

export const createUsuario = (usuarioData) => {
  const formData = new FormData();
  formData.append('nombre', usuarioData.nombre);
  formData.append('apellido', usuarioData.apellido);
  formData.append('correo', usuarioData.correo);
  formData.append('contraseña', usuarioData.contraseña);
  formData.append('rol', usuarioData.rol);
  if (usuarioData.imagen_perfil) {
    formData.append('imagen_perfil', usuarioData.imagen_perfil);
  }
  return api.post('/usuarios/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const updateUsuario = (idUsuario, usuarioData) => {
  const formData = new FormData();
  formData.append('nombre', usuarioData.nombre);
  formData.append('apellido', usuarioData.apellido);
  formData.append('correo', usuarioData.correo);
  formData.append('contraseña', usuarioData.contraseña);
  formData.append('rol', usuarioData.rol);
  if (usuarioData.imagen_perfil instanceof File) {
    formData.append('imagen_perfil', usuarioData.imagen_perfil);
  }
  return api.put(`/usuarios/${idUsuario}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteUsuario = (idUsuario) => {
  return api.delete(`/usuarios/${idUsuario}/`);
};

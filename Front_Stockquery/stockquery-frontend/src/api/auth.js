import api from './apiConfig';

/**
 * Inicia sesión con correo y contraseña
 * @param {string} correo
 * @param {string} contraseña
 * @returns {Promise<Object>} data de usuario
 */
export const loginUser = async (correo, contraseña) => {
  const response = await api.post('/login/', { correo, contraseña });
  return response.data;
};

/**
 * Obtiene la información del usuario autenticado
 * @returns {Promise<Object>} data de usuario
 */
export const getUsuarioInfo = async () => {
  const response = await api.get('/usuario_info/');
  return response.data;
};

/**
 * Cierra la sesión
 * @returns {Promise<Object>}
 */
export const logoutUser = async () => {
  const response = await api.post('/logout/');
  return response.data;
};
